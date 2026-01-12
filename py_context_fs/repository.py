import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple
from uuid import uuid4

from .core import ContextFile, ContextSource

_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


@dataclass
class RepositoryRecord:
    """Persistent record stored in the repository."""

    views: Dict[str, str]
    metadata: Dict[str, Any]
    updated_at: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "views": self.views,
            "metadata": self.metadata,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "RepositoryRecord":
        views = data.get("views", {})
        metadata = data.get("metadata", {})
        updated_at = float(data.get("updated_at", time.time()))
        return RepositoryRecord(views=views, metadata=metadata, updated_at=updated_at)


class PersistentContextRepository(ContextSource):
    """Persistent history/memory/scratchpad repository with basic indexing.

    Paths are rooted by layer: "history/...", "memory/...", "scratchpad/...".
    Records are stored as JSON with multiple views.
    """

    def __init__(self, root_dir: str):
        self._root = Path(root_dir)
        self._layers = {
            "history": self._root / "history",
            "memory": self._root / "memory",
            "scratchpad": self._root / "scratchpad",
        }
        for layer_dir in self._layers.values():
            layer_dir.mkdir(parents=True, exist_ok=True)

        self._memory_index: Dict[str, Set[str]] = {}
        self._memory_tokens: Dict[str, Set[str]] = {}
        self.rebuild_index()

    def read(self, path: str, view: str = "default") -> ContextFile:
        layer, rel = self._split_path(path)
        record_path = self._record_path(layer, rel)
        record = self._load_record(record_path)

        if view not in record.views:
            raise ValueError(f"View '{view}' not found for file {path}")

        return ContextFile(content=record.views[view], metadata=record.metadata)

    def list(self, path: str) -> List[str]:
        layer, rel = self._split_path(path)
        prefix = rel.as_posix().strip("/")

        results: List[str] = []
        for file_path in self._layers[layer].rglob("*.json"):
            rel_path = file_path.relative_to(self._layers[layer]).as_posix()
            if prefix and not rel_path.startswith(prefix):
                continue
            results.append(f"{layer}/{rel_path}")
        return results

    def search(self, query: str) -> List[str]:
        results: Set[str] = set()
        tokens = self._tokenize(query)

        if tokens:
            # Indexed search for memory layer
            for token in tokens:
                for path in self._memory_index.get(token, set()):
                    results.add(path)

        # Fallback substring search for history and scratchpad layers
        for layer in ("history", "scratchpad"):
            for file_path in self._layers[layer].rglob("*.json"):
                record = self._load_record(file_path)
                if any(query in view for view in record.views.values()):
                    rel_path = file_path.relative_to(self._layers[layer]).as_posix()
                    results.add(f"{layer}/{rel_path}")

        return sorted(results)

    def write(self, path: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.write_view(path, view="default", content=content, metadata=metadata)

    def write_view(
        self,
        path: str,
        view: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        layer, rel = self._split_path(path)
        record_path = self._record_path(layer, rel)
        record_path.parent.mkdir(parents=True, exist_ok=True)

        if record_path.exists():
            record = self._load_record(record_path)
        else:
            record = RepositoryRecord(views={}, metadata={}, updated_at=time.time())

        record.views[view] = content
        if metadata is not None:
            record.metadata = metadata
        record.updated_at = time.time()
        self._save_record(record_path, record)

        if layer == "memory":
            self._update_memory_index(f"{layer}/{rel.as_posix()}", record.views.get("default", ""))

    def append_history(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Appends an immutable history entry and returns its path."""
        entry_id = f"{int(time.time())}_{uuid4().hex}"
        path = f"history/{entry_id}.json"
        self.write(path, content, metadata=metadata)
        return path

    def persist_scratchpad(
        self, content: str, metadata: Optional[Dict[str, Any]] = None, key: Optional[str] = None
    ) -> str:
        """Writes to scratchpad and returns its path."""
        entry_id = key or uuid4().hex
        path = f"scratchpad/{entry_id}.json"
        self.write(path, content, metadata=metadata)
        return path

    def commit_scratchpad_to_history(
        self, scratchpad_path: str, metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Moves scratchpad content into history with provenance metadata."""
        record = self.read(scratchpad_path)
        merged_meta = dict(record.metadata)
        if metadata:
            merged_meta.update(metadata)
        merged_meta.setdefault("source", scratchpad_path)
        return self.append_history(record.content, metadata=merged_meta)

    def promote_history_to_memory(
        self,
        history_path: str,
        memory_key: str,
        transform: Optional[Callable[[str], str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Promotes a history record into memory, optionally transforming content."""
        record = self.read(history_path)
        content = transform(record.content) if transform else record.content
        merged_meta = dict(record.metadata)
        if metadata:
            merged_meta.update(metadata)
        merged_meta.setdefault("source", history_path)
        memory_path = f"memory/{memory_key}.json"
        self.write(memory_path, content, metadata=merged_meta)
        return memory_path

    def rebuild_index(self) -> None:
        """Rebuilds the in-memory index for memory layer."""
        self._memory_index.clear()
        self._memory_tokens.clear()
        for file_path in self._layers["memory"].rglob("*.json"):
            rel_path = file_path.relative_to(self._layers["memory"]).as_posix()
            record = self._load_record(file_path)
            self._update_memory_index(f"memory/{rel_path}", record.views.get("default", ""))

    def _split_path(self, path: str) -> Tuple[str, Path]:
        rel_path = Path(path)
        parts = rel_path.parts
        if not parts:
            raise ValueError("Path must include a layer prefix (history/memory/scratchpad)")
        layer = parts[0]
        if layer not in self._layers:
            raise ValueError(f"Unknown layer '{layer}'")
        remainder = Path(*parts[1:]) if len(parts) > 1 else Path("")
        return layer, remainder

    def _record_path(self, layer: str, rel: Path) -> Path:
        if not rel.as_posix() or rel.as_posix() == ".":
            raise ValueError("Path must include a file name")
        if rel.suffix != ".json":
            rel = rel.with_suffix(".json")
        return self._layers[layer] / rel

    def _load_record(self, path: Path) -> RepositoryRecord:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return RepositoryRecord.from_dict(data)

    def _save_record(self, path: Path, record: RepositoryRecord) -> None:
        with path.open("w", encoding="utf-8") as handle:
            json.dump(record.to_dict(), handle, ensure_ascii=True, indent=2)

    def _update_memory_index(self, path: str, content: str) -> None:
        tokens = self._tokenize(content)
        old_tokens = self._memory_tokens.get(path, set())

        for token in old_tokens - tokens:
            self._memory_index.get(token, set()).discard(path)
        for token in tokens - old_tokens:
            self._memory_index.setdefault(token, set()).add(path)

        self._memory_tokens[path] = tokens

    def _tokenize(self, text: str) -> Set[str]:
        return {match.group(0).lower() for match in _TOKEN_RE.finditer(text)}
