import sys
import os

# Ensure the package is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from py_context_fs.core import ContextRouter
from py_context_fs.pipeline import ContextConstructor, ContextLoader
from py_context_fs.repository import PersistentContextRepository


def main():
    print("Initializing persistent repository demo...")

    repo_root = os.path.join(os.path.dirname(__file__), "context_repo_persistent")
    repo = PersistentContextRepository(repo_root)

    # 1. Append history and promote to memory (creates JSON files on disk)
    history_path = repo.append_history(
        "User asked for a physical file demo.", metadata={"actor": "user"}
    )
    memory_path = repo.promote_history_to_memory(history_path, memory_key="session_002")

    # 2. Mount the repository and construct a manifest
    fs = ContextRouter()
    fs.mount("/context", repo)

    constructor = ContextConstructor(fs)
    manifest = constructor.construct(paths=[f"/context/{memory_path}"])

    # 3. Load with a generous token budget
    loader = ContextLoader(fs)
    context = loader.load(manifest, max_tokens=200)

    print("\n[Generated Context START]")
    print(context)
    print("[Generated Context END]\n")

    # 4. Show where the physical file lives
    print("Persistent files created under:")
    print(repo_root)
    print("History file:")
    print(os.path.join(repo_root, history_path))
    print("Memory file:")
    print(os.path.join(repo_root, memory_path))


if __name__ == "__main__":
    main()
