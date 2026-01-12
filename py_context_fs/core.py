import abc
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import os

@dataclass
class ContextFile:
    """Represents a virtual file in the Agentic File System."""
    content: str
    metadata: Dict[str, Any]
    token_count: Optional[int] = None

class ContextSource(abc.ABC):
    """Abstract base class for sources in the Context File System."""

    @abc.abstractmethod
    def read(self, path: str, view: str = "default") -> ContextFile:
        """Reads a virtual file.

        Args:
            path: The relative path to the file within this node.
            view: The view to read (e.g., 'default', 'summary').

        Returns:
            A ContextFile object.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        pass

    @abc.abstractmethod
    def list(self, path: str) -> List[str]:
        """Lists virtual files in the given path.

        Args:
            path: The relative path to list.

        Returns:
            A list of file names/paths.
        """
        pass

    @abc.abstractmethod
    def search(self, query: str) -> List[str]:
        """Searches for files matching the query.

        Args:
            query: The search query.

        Returns:
            A list of matching paths.
        """
        pass

    @abc.abstractmethod
    def write(self, path: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Writes content to a virtual file.

        Args:
            path: The relative path to write to.
            content: The content to write.
            metadata: Optional metadata to save.
        """
        pass

class ContextRouter:
    """The Router for the Agentic File System.

    Mounts ContextSources at specific prefixes and routes operations to them.
    """

    def __init__(self):
        self._mounts: Dict[str, ContextSource] = {}

    def mount(self, path_prefix: str, node: ContextSource) -> None:
        """Mounts a ContextSource at a specific path prefix.

        Args:
            path_prefix: The prefix to mount at (e.g., '/student').
                         Must start with '/'.
            node: The ContextSource to mount.
        """
        if not path_prefix.startswith("/"):
            raise ValueError("Path prefix must start with '/'")
        # Ensure prefix doesn't end with / unless it's just root (though usually we want distinct mounts)
        if path_prefix != "/" and path_prefix.endswith("/"):
            path_prefix = path_prefix.rstrip("/")
        
        self._mounts[path_prefix] = node

    def _resolve(self, path: str) -> tuple[ContextSource, str]:
        """Resolves a full path to a (node, relative_path) tuple.

        Args:
            path: The full path (e.g., '/student/transcript.txt').

        Returns:
            Tuple of (ContextSource, relative_path).

        Raises:
            FileNotFoundError: If no mount point matches the path.
        """
        if not path.startswith("/"):
             raise ValueError("Path must be absolute (start with '/')")

        # Sort mounts by length (descending) to match specific prefixes first
        sorted_mounts = sorted(self._mounts.keys(), key=len, reverse=True)

        for mount_point in sorted_mounts:
            if path == mount_point or path.startswith(mount_point + "/"):
                node = self._mounts[mount_point]
                # specific case for root mount
                if mount_point == "/":
                    rel_path = path[1:] # strip leading /
                else:
                    rel_path = path[len(mount_point):].lstrip("/")
                return node, rel_path

        raise FileNotFoundError(f"No mount point found for path: {path}")

    def open(self, path: str, view: str = "default") -> ContextFile:
        """Opens a virtual file.

        Args:
            path: The full path to the file.
            view: The view to read.

        Returns:
            A ContextFile object.
        """
        node, rel_path = self._resolve(path)
        return node.read(rel_path, view=view)

    def list(self, path: str) -> List[str]:
         """Lists files at a given path."""
         node, rel_path = self._resolve(path)
         return node.list(rel_path)
    
    def search(self, query: str) -> List[str]:
        """Global search across all mounts (naive implementation).
        
        For a real system, you might want to only search specific mounts or parallelize.
        Here we'll iterate all mounts.
        """
        results = []
        for mount_point, node in self._mounts.items():
            # This is a bit simplistic as search logic might vary per node
            # We assume node.search returns relative paths, so we prepend mount point
            node_results = node.search(query)
            for res in node_results:
                full_path = f"{mount_point}/{res}".replace("//", "/")
                results.append(full_path)
        return results

    def exists(self, path: str) -> bool:
        """Checks if a file exists."""
        try:
            self.open(path) # Try reading default view. Optimization: Add exists to ContextSource
            return True
        except (FileNotFoundError, ValueError):
            return False

    def write(self, path: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Writes to a virtual file."""
        node, rel_path = self._resolve(path)
        node.write(rel_path, content, metadata)
