import tiktoken
from dataclasses import dataclass, field
from typing import List, Optional, Any, Callable
from .core import ContextRouter, ContextFile

@dataclass
class ContextManifest:
    """Ordered list of files to attempt to load."""
    files: List[str] = field(default_factory=list)

class ContextConstructor:
    """Component A: Selection."""

    def __init__(self, fs: ContextRouter):
        self._fs = fs

    def construct(self, query: str = None, paths: List[str] = None) -> ContextManifest:
        """Constructs a manifest based on search query or explicit paths.

        Args:
            query: Optional search query.
            paths: Optional list of explicit paths.

        Returns:
            A ContextManifest.
        """
        manifest = ContextManifest()
        
        if paths:
            manifest.files.extend(paths)
        
        if query:
            # In a real impl, we might deduplicate
            results = self._fs.search(query)
            for res in results:
                if res not in manifest.files:
                    manifest.files.append(res)
        
        return manifest

class ContextLoader:
    """Component B: Token Budgeting & Streaming."""

    def __init__(self, fs: ContextRouter, model: str = "gpt-4"):
        self._fs = fs
        self._encoding = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str) -> int:
        return len(self._encoding.encode(text))

    def load(self, manifest: ContextManifest, max_tokens: int) -> str:
        """Loads context from the manifest, respecting the token budget.

        Uses a naive Knapsack-like approach: fills until full.
        Falls back to 'summary' view if 'default' view is too large (heuristic).
        """
        final_context_parts = []
        current_tokens = 0
        
        for path in manifest.files:
            try:
                # 1. Try default view
                file_obj = self._fs.open(path, view="default")
                content = file_obj.content
                tokens = self.count_tokens(content) # Naive exact count
            except (ValueError, FileNotFoundError):
                # Default view unavailable; try summary view instead
                try:
                    summary_file = self._fs.open(path, view="summary")
                    summary_content = summary_file.content
                    summary_tokens = self.count_tokens(summary_content)
                    if current_tokens + summary_tokens <= max_tokens:
                        final_context_parts.append(
                            f"--- File: {path} (Summary) ---\n{summary_content}\n"
                        )
                        current_tokens += summary_tokens
                    continue
                except (ValueError, FileNotFoundError):
                    continue

            if current_tokens + tokens <= max_tokens:
                final_context_parts.append(f"--- File: {path} ---\n{content}\n")
                current_tokens += tokens
            else:
                # 2. Compression Strategy: Try summary view
                try:
                    summary_file = self._fs.open(path, view="summary")
                    summary_content = summary_file.content
                    summary_tokens = self.count_tokens(summary_content)
                    
                    if current_tokens + summary_tokens <= max_tokens:
                        final_context_parts.append(f"--- File: {path} (Summary) ---\n{summary_content}\n")
                        current_tokens += summary_tokens
                    else:
                        # 3. Truncation or Skip. For now, we skip to save partial context integrity
                        # or we could add a note about omitted file
                        pass
                except (ValueError, FileNotFoundError):
                    # No summary view available, just skip
                    pass
        
        return "\n".join(final_context_parts)

class ContextEvaluator:
    """Component C: Validation & Persistence."""

    def __init__(self, fs: ContextRouter):
        self._fs = fs

    def evaluate(self, response: str, validator: Callable[[str], bool], output_path: str) -> bool:
        """Validates the response and saves it if valid.

        Args:
            response: The LLM's response string.
            validator: A function that returns True if valid.
            output_path: Path to save the valid response to.

        Returns:
            True if valid and saved, False otherwise.
        """
        if validator(response):
             self._fs.write(output_path, response, metadata={"valid": True})
             return True
        return False
