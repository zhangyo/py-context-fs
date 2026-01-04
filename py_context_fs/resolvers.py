from typing import Any, Dict, List, Optional
from .core import ContextNode, ContextFile

class DictResolver(ContextNode):
    """An in-memory implementation of ContextNode using a Python dictionary.
    
    Structure of data:
    {
        "file_path": {
            "default": "full content",
            "summary": "short summary",
            ... other views
        }
    }
    """

    def __init__(self, check_metadata: bool = False):
        self._data: Dict[str, Dict[str, str]] = {}
        # Simple storage for metadata if checking is needed, 
        # heavily simplified for this reference implementation
        self._metadata: Dict[str, Dict[str, Any]] = {} 

    def populate(self, path: str, views: Dict[str, str], metadata: Optional[Dict[str, Any]] = None):
        """Helper to populate data for testing."""
        self._data[path] = views
        if metadata:
            self._metadata[path] = metadata

    def read(self, path: str, view: str = "default") -> ContextFile:
        if path not in self._data:
             raise FileNotFoundError(f"File not found: {path}")
        
        views = self._data[path]
        if view not in views:
            # Fallback logic could go here, but for now be strict
             raise ValueError(f"View '{view}' not found for file {path}")
        
        content = views[view]
        meta = self._metadata.get(path, {})
        
        return ContextFile(content=content, metadata=meta)

    def list(self, path: str) -> List[str]:
        # Naive list implementation: returns all keys that start with path 
        # In a real FS, this would handle directories properly
        results = []
        # Normalizing path for simple prefix matching
        prefix = path if path.endswith("/") or path == "" else f"{path}/"
        if path == "" or path == ".": # root of this node
             prefix = ""

        seen_roots = set()

        for key in self._data.keys():
            if prefix == "" or key.startswith(prefix):
                # Return relative path from the listing directory
                # e.g. path="", key="foo.txt" -> "foo.txt"
                # e.g. path="sub", key="sub/bar.txt" -> "bar.txt" (if we want just filenames)
                # For this simple dict resolver, let's just return the full relative paths matching
                results.append(key)
        return results

    def search(self, query: str) -> List[str]:
        results = []
        for path, views in self._data.items():
            # Search in default view content
            if "default" in views and query in views["default"]:
                results.append(path)
        return results

    def write(self, path: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        if path not in self._data:
            self._data[path] = {}
        
        self._data[path]["default"] = content
        if metadata:
             self._metadata[path] = metadata

class ReadOnlyWrapper(ContextNode):
    """Wrapper that prevents write operations."""

    def __init__(self, wrapped: ContextNode):
        self._wrapped = wrapped

    def read(self, path: str, view: str = "default") -> ContextFile:
        return self._wrapped.read(path, view)

    def list(self, path: str) -> List[str]:
        return self._wrapped.list(path)

    def search(self, query: str) -> List[str]:
        return self._wrapped.search(query)

    def write(self, path: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        raise PermissionError(f"Write operation not allowed on ReadOnlyWrapper for path: {path}")
