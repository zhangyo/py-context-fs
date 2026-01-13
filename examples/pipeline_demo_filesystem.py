import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure the package is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from py_context_fs.core import ContextFile, ContextRouter, ContextSource
from py_context_fs.pipeline import ContextConstructor, ContextLoader


class LocalFileResolver(ContextSource):
    """Context source backed by a local directory.

    Summary view uses the naming convention: "<name>.summary<suffix>".
    Example: transcript.txt -> transcript.summary.txt
    """

    def __init__(self, root_dir: str):
        self._root = Path(root_dir)
        self._root.mkdir(parents=True, exist_ok=True)

    def read(self, path: str, view: str = "default") -> ContextFile:
        file_path = self._resolve_path(path, view=view)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path} (view={view})")
        content = file_path.read_text(encoding="utf-8")
        return ContextFile(content=content, metadata={"path": str(file_path)})

    def list(self, path: str) -> List[str]:
        base = self._root / path
        if base.is_file():
            return [path]
        results = []
        if base.exists():
            for file_path in base.rglob("*"):
                if file_path.is_file():
                    results.append(file_path.relative_to(self._root).as_posix())
        return results

    def search(self, query: str) -> List[str]:
        results = []
        for file_path in self._root.rglob("*"):
            if not file_path.is_file():
                continue
            content = file_path.read_text(encoding="utf-8")
            if query in content:
                results.append(file_path.relative_to(self._root).as_posix())
        return results

    def write(self, path: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        file_path = self._resolve_path(path, view="default")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

    def _resolve_path(self, path: str, view: str) -> Path:
        base = self._root / path
        if view == "default":
            return base
        return base.with_name(f"{base.stem}.{view}{base.suffix}")


def main():
    print("Initializing filesystem-backed demo...")

    student_root = os.path.join(os.path.dirname(__file__), "student_files")
    resolver = LocalFileResolver(student_root)

    long_transcript = "This is a very long transcript of a lecture " * 100
    short_summary = "Lecture covered: Basics of AFS."

    resolver.write("transcript.txt", long_transcript)
    Path(student_root, "transcript.summary.txt").write_text(short_summary, encoding="utf-8")

    resolver.write("syllabus.txt", "Module 1: Intro\nModule 2: Advanced")
    Path(student_root, "syllabus.summary.txt").write_text("M1, M2", encoding="utf-8")

    fs = ContextRouter()
    fs.mount("/student", resolver)
    print("Mounted LocalFileResolver at /student")
    print(f"Student files directory: {student_root}")

    # Demonstrate list
    print("\n--- VFS list() demo ---")
    listed = fs.list("/student")
    print("Listed files:")
    for item in sorted(listed):
        print(f"- {item}")

    # Demonstrate search
    print("\n--- VFS search() demo ---")
    matches = fs.search("Basics of AFS")
    print("Search results for 'Basics of AFS':")
    for match in sorted(matches):
        print(f"- {match}")

    # Demonstrate read (default and summary views)
    print("\n--- VFS read() demo ---")
    transcript_default = fs.open("/student/transcript.txt", view="default")
    transcript_summary = fs.open("/student/transcript.txt", view="summary")
    print("Transcript default (first 80 chars):")
    print(transcript_default.content[:80] + "...")
    print("Transcript summary:")
    print(transcript_summary.content)

    constructor = ContextConstructor(fs)
    manifest = constructor.construct(
        paths=["/student/transcript.txt", "/student/syllabus.txt"]
    )

    loader = ContextLoader(fs)
    context = loader.load(manifest, max_tokens=200)

    print("\n[Generated Context START]")
    print(context)
    print("[Generated Context END]")


if __name__ == "__main__":
    main()
