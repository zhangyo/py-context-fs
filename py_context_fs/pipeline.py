import re
import time
import tiktoken
from dataclasses import dataclass, field
from typing import List, Optional, Any, Callable, Dict, Iterable, Sequence
from .core import ContextRouter, ContextFile

@dataclass
class ContextManifest:
    """Ordered list of files to attempt to load."""
    files: List[str] = field(default_factory=list)
    entries: List["ContextManifestEntry"] = field(default_factory=list)

@dataclass
class ContextManifestEntry:
    """Represents a selected file with optional priority and view preference."""
    path: str
    priority: float = 0.0
    preferred_view: Optional[str] = None
    estimated_tokens: Optional[int] = None

@dataclass
class SelectionCriteria:
    """Selection criteria for constructing a manifest.

    Attributes:
        query: Optional search query.
        paths: Optional list of explicit paths.
        include_patterns: Regex patterns to include.
        exclude_patterns: Regex patterns to exclude.
        metadata_filter: Predicate to filter using file metadata.
        ranker: Function that assigns a priority score per file.
        max_results: Maximum number of files to include.
        max_tokens: Optional token budget for selection (approximate).
        token_counter: Optional function to estimate token cost.
        preferred_view: Preferred view to request (e.g., "summary").
        view_selector: Function to select a preferred view based on metadata.
    """
    query: Optional[str] = None
    paths: Optional[List[str]] = None
    include_patterns: Optional[List[str]] = None
    exclude_patterns: Optional[List[str]] = None
    metadata_filter: Optional[Callable[[Dict[str, Any]], bool]] = None
    ranker: Optional[Callable[[str, Dict[str, Any]], float]] = None
    max_results: Optional[int] = None
    max_tokens: Optional[int] = None
    token_counter: Optional[Callable[[str], int]] = None
    preferred_view: Optional[str] = None
    view_selector: Optional[Callable[[Dict[str, Any]], Optional[str]]] = None

class ContextConstructor:
    """Component A: Selection."""

    def __init__(self, fs: ContextRouter):
        self._fs = fs

    def _matches_patterns(self, path: str, patterns: Optional[List[str]]) -> bool:
        if not patterns:
            return True
        return any(re.search(pattern, path) for pattern in patterns)

    def _open_for_metadata(self, path: str) -> Optional[ContextFile]:
        try:
            return self._fs.open(path, view="default")
        except (ValueError, FileNotFoundError):
            try:
                return self._fs.open(path, view="summary")
            except (ValueError, FileNotFoundError):
                return None

    def _open_for_estimation(
        self,
        path: str,
        preferred_view: Optional[str],
    ) -> Optional[ContextFile]:
        if preferred_view:
            try:
                return self._fs.open(path, view=preferred_view)
            except (ValueError, FileNotFoundError):
                pass
        try:
            return self._fs.open(path, view="summary")
        except (ValueError, FileNotFoundError):
            try:
                return self._fs.open(path, view="default")
            except (ValueError, FileNotFoundError):
                return None

    def _select_preferred_view(
        self,
        metadata: Dict[str, Any],
        criteria: SelectionCriteria,
    ) -> Optional[str]:
        if criteria.view_selector:
            return criteria.view_selector(metadata)
        if criteria.preferred_view:
            return criteria.preferred_view
        return metadata.get("preferred_view")

    def construct(
        self,
        criteria: Optional[SelectionCriteria] = None,
        query: str = None,
        paths: List[str] = None,
    ) -> ContextManifest:
        """Constructs a manifest based on search query or explicit paths.

        Args:
            criteria: Optional selection criteria (filters, ranking, compression hints).
            query: Optional search query.
            paths: Optional list of explicit paths.

        Returns:
            A ContextManifest.
        """
        criteria = criteria or SelectionCriteria()
        search_query = criteria.query if criteria.query is not None else query

        candidate_paths = []
        if criteria.paths:
            candidate_paths.extend(criteria.paths)
        if paths:
            candidate_paths.extend(paths)
        if search_query:
            candidate_paths.extend(self._fs.search(search_query))

        deduped = {}
        for path in candidate_paths:
            if path not in deduped:
                deduped[path] = None

        include_patterns = criteria.include_patterns
        exclude_patterns = criteria.exclude_patterns

        entries: List[ContextManifestEntry] = []
        for path in deduped.keys():
            if include_patterns and not self._matches_patterns(path, include_patterns):
                continue
            if exclude_patterns and self._matches_patterns(path, exclude_patterns):
                continue

            file_obj = self._open_for_metadata(path)
            if file_obj is None:
                continue

            metadata = file_obj.metadata or {}
            if criteria.metadata_filter and not criteria.metadata_filter(metadata):
                continue

            ranker = criteria.ranker or (lambda _, meta: float(meta.get("priority", 0.0)))
            priority = ranker(path, metadata)
            preferred_view = self._select_preferred_view(metadata, criteria)
            estimated_tokens = None
            if criteria.max_tokens is not None:
                meta_tokens = metadata.get("token_count")
                if isinstance(meta_tokens, int):
                    estimated_tokens = meta_tokens
                else:
                    token_counter = criteria.token_counter or (lambda text: len(text.split()))
                    estimation_file = self._open_for_estimation(path, preferred_view)
                    if estimation_file is not None:
                        estimated_tokens = token_counter(estimation_file.content)
            entries.append(ContextManifestEntry(
                path=path,
                priority=priority,
                preferred_view=preferred_view,
                estimated_tokens=estimated_tokens,
            ))

        entries.sort(key=lambda entry: entry.priority, reverse=True)
        if criteria.max_results is not None:
            entries = entries[:criteria.max_results]

        if criteria.max_tokens is not None:
            budgeted = []
            current_tokens = 0
            for entry in entries:
                if entry.estimated_tokens is None:
                    budgeted.append(entry)
                    continue
                if current_tokens + entry.estimated_tokens > criteria.max_tokens:
                    continue
                budgeted.append(entry)
                current_tokens += entry.estimated_tokens
            entries = budgeted

        return ContextManifest(
            files=[entry.path for entry in entries],
            entries=entries,
        )

class ContextLoader:
    """Component B: Token Budgeting & Streaming."""

    def __init__(self, fs: ContextRouter, model: str = "gpt-4"):
        self._fs = fs
        self._encoding = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str) -> int:
        return len(self._encoding.encode(text))

    def _format_header(self, path: str, view: str) -> str:
        if view == "summary":
            return f"--- File: {path} (Summary) ---"
        return f"--- File: {path} ---"

    def _select_entries(self, manifest: ContextManifest, max_tokens: int) -> List[Dict[str, Any]]:
        """Selects file entries to include, honoring the token budget."""
        selections = []

        entries = manifest.entries or [
            ContextManifestEntry(path=path) for path in manifest.files
        ]
        for entry in entries:
            path = entry.path
            options = []
            try:
                default_file = self._fs.open(path, view="default")
                default_content = default_file.content
                default_header = self._format_header(path, "default")
                default_tokens = self.count_tokens(
                    f"{default_header}\n{default_content}\n"
                )
                default_value = 2.0 + entry.priority
                if entry.preferred_view == "default":
                    default_value += 1.0
                options.append({
                    "path": path,
                    "view": "default",
                    "header": default_header,
                    "content": default_content,
                    "tokens": default_tokens,
                    "value": default_value,
                })
            except (ValueError, FileNotFoundError):
                pass

            try:
                summary_file = self._fs.open(path, view="summary")
                summary_content = summary_file.content
                summary_header = self._format_header(path, "summary")
                summary_tokens = self.count_tokens(
                    f"{summary_header}\n{summary_content}\n"
                )
                summary_value = 1.0 + entry.priority
                if entry.preferred_view == "summary":
                    summary_value += 1.0
                options.append({
                    "path": path,
                    "view": "summary",
                    "header": summary_header,
                    "content": summary_content,
                    "tokens": summary_tokens,
                    "value": summary_value,
                })
            except (ValueError, FileNotFoundError):
                pass

            selections.append(options)

        dp = {0: (0, [])}
        for options in selections:
            next_dp = dict(dp)
            for current_tokens, (current_value, current_selection) in dp.items():
                for option in options:
                    new_tokens = current_tokens + option["tokens"]
                    if new_tokens > max_tokens:
                        continue
                    new_value = current_value + option["value"]
                    existing = next_dp.get(new_tokens)
                    if existing is None or new_value > existing[0]:
                        next_dp[new_tokens] = (new_value, current_selection + [option])
            dp = next_dp

        best_tokens = 0
        best_value = -1
        best_selection = []
        for tokens_used, (value, selection) in dp.items():
            if value > best_value or (value == best_value and tokens_used > best_tokens):
                best_value = value
                best_tokens = tokens_used
                best_selection = selection

        return best_selection

    def load_stream(self, manifest: ContextManifest, max_tokens: int) -> Iterable[str]:
        """Streams context chunks from the manifest, respecting the token budget.

        Yields file-sized chunks so callers can interleave safety checks or abort early.
        """
        for selection in self._select_entries(manifest, max_tokens):
            header = selection.get("header") or self._format_header(
                selection["path"],
                selection["view"],
            )
            yield f"{header}\n{selection['content']}\n"

    def load(self, manifest: ContextManifest, max_tokens: int) -> str:
        """Loads context from the manifest, respecting the token budget.

        This aggregates streamed chunks into a single string.
        """
        return "\n".join(self.load_stream(manifest, max_tokens))

class ContextEvaluator:
    """Component C: Validation & Persistence."""

    def __init__(self, fs: ContextRouter):
        self._fs = fs

    def evaluate(
        self,
        response: str,
        validator: Callable[[str], bool],
        output_path: str,
        validator_name: Optional[str] = None,
        evidence_paths: Optional[Sequence[str]] = None,
        decision_metadata: Optional[Dict[str, Any]] = None,
        reviewed_at: Optional[float] = None,
    ) -> bool:
        """Validates the response and saves it if valid.

        Args:
            response: The LLM's response string.
            validator: A function that returns True if valid.
            output_path: Path to save the valid response to.
            validator_name: Optional identifier for the validator used.
            evidence_paths: Optional list of evidence paths used for validation.
            decision_metadata: Optional extra metadata for auditability.
            reviewed_at: Optional UNIX timestamp for validation time.

        Returns:
            True if valid and saved, False otherwise.
        """
        if validator(response):
             metadata = {
                 "valid": True,
                 "validator": validator_name,
                 "evidence": list(evidence_paths) if evidence_paths else None,
                 "reviewed_at": reviewed_at if reviewed_at is not None else time.time(),
             }
             if decision_metadata:
                 metadata.update(decision_metadata)
             self._fs.write(output_path, response, metadata=metadata)
             return True
        return False
