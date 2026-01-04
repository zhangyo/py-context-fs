# py-context-fs

A Python implementation of the **Agentic File System (AFS)** pattern and **Context Engineering Pipeline**, based on the research paper *"Everything is Context"*.

This library decouples **Data Access** (Virtual File System) from **Context Management** (Pipeline), allowing agents to dynamically select, compress, and load context into LLM token windows.


## Installation

You can install `py-context-fs` directly from the source:

```bash
# Install via pip
pip install git+https://github.com/yourusername/py-context-fs.git

# Or clone and install locally (for development)
git clone https://github.com/yourusername/py-context-fs.git
cd py-context-fs
pip install -e .
```


## Core Concepts

### 1. The Virtual File System (VFS)
Treats all data sources (databases, APIs, memory) as files.
- **`ContextFS`**: The router that mounts nodes at paths (e.g., `/student`, `/db`).
- **`ContextNode`**: Abstract adapter for data sources. Implement this to connect to SQL, Vector DBs, or APIs.
- **`ContextFile`**: Represents data with `content`, `metadata`, and optional `token_count`. Supports multiple "views" (e.g., `default`, `summary`) for compression.

#### Standard Operations
The VFS enforces a strict interface for all data sources, mimicking POSIX-like behavior:
- **`list(path)`**: Discovering available resources (e.g., listing all assessments for a student).
- **`read(path)`**: Retrieving the content of a resource (e.g., reading the transcript of a specific quiz).
- **`write(path, content)`**: Updating the state (e.g., modifying the student's mastery profile).
- **`search(query)`**: A specialized operation mapped to vector database lookups.

### 2. The Pipeline
Manages the flow of data to the LLM.
- **`ContextConstructor`**: Selects relevant files to load (via search, rules, or explicit paths).
- **`ContextLoader`**: Fits files into a strict token budget (Knapsack algorithm). It uses `tiktoken` to count tokens and automatically falls back to smaller views (e.g., "summary") if the default content is too large.
- **`ContextEvaluator`**: Validates agent outputs (e.g., JSON schema) and persists results back to the VFS.

## Usage

### Basic File System Operations

```python
from py_context_fs.core import ContextFS
from py_context_fs.resolvers import DictResolver

# 1. Initialize FS
fs = ContextFS()

# 2. Mount a data source (Resolver)
# In a real app, this might be a SQLResolver or APIResolver
resolver = DictResolver()
resolver.populate("notes.txt", {
    "default": "Full text of the meeting notes...",
    "summary": "Meeting summary."
})
fs.mount("/work", resolver)

# 3. Read files
file = fs.open("/work/notes.txt", view="default")
print(file.content)
```

### Full Pipeline Example

```python
from py_context_fs.pipeline import ContextConstructor, ContextLoader

# 1. Selection (Stage A)
constructor = ContextConstructor(fs)
manifest = constructor.construct(paths=["/work/notes.txt"])

# 2. Loading with Token Budget (Stage B)
# Automatically chooses views to fit max_tokens
loader = ContextLoader(fs, model="gpt-4")
context_string = loader.load(manifest, max_tokens=500)
```

## Database Integration (Virtualizing Databases)

The VFS can treat databases as file systems by mapping paths to queries:

- **Path**: `/users/123` → `SELECT * FROM users WHERE id = 123`
- **View**: `view="summary"` → `SELECT summary FROM ...`

### Example Implementation

```python
class DatabaseResolver(ContextNode):
    def __init__(self, db_connection):
        self.db = db_connection

    def read(self, path: str, view: str = "default") -> ContextFile:
        # 1. Translate path to DB identifier
        record_id = path
        
        # 2. Query the database
        record = self.db.execute("SELECT * FROM rules WHERE name = ?", (record_id,))
        
        # 3. Handle Views
        content = record['summary'] if view == "summary" else record['full_text']

        return ContextFile(content=content, metadata={"source": "postgres"})

    def list(self, path: str) -> List[str]:
        return [row['name'] for row in self.db.execute("SELECT name FROM rules")]
```

## Running the Demo

A complete runnable example is provided in `examples/pipeline_demo.py`. This script demonstrates the full flow: mounting a data source, populating it with disparate views, and running the pipeline to see automatic compression in action.

```bash
python3 examples/pipeline_demo.py
```

## Project Structure

- `py_context_fs/core.py`: Abstract interfaces and the Router.
- `py_context_fs/pipeline.py`: The Constructor, Loader, and Evaluator.
- `py_context_fs/resolvers.py`: Reference implementations (DictResolver).
