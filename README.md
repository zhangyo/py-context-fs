# py-context-fs

A Python implementation of the **Agentic File System (AFS)** pattern and **Context Engineering Pipeline**, based on the research paper *"Everything is Context"*.

This library decouples **Data Access** (Virtual File System) from **Context Management** (Pipeline), allowing agents to dynamically select, compress, and load context into LLM token windows.

## Installation

```bash
pip install -r requirements.txt
```

## Core Concepts

### 1. The Virtual File System (VFS)
Treats all data sources (databases, APIs, memory) as files.
- **`ContextFS`**: The router that mounts nodes at paths (e.g., `/student`, `/db`).
- **`ContextNode`**: Abstract adapter for data sources. Implement this to connect to SQL, Vector DBs, or APIs.
- **`ContextFile`**: Represents data with `content`, `metadata`, and optional `token_count`. Supports multiple "views" (e.g., `default`, `summary`) for compression.

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

## Running the Demo

A complete runnable example is provided in `examples/pipeline_demo.py`. This script demonstrates the full flow: mounting a data source, populating it with disparate views, and running the pipeline to see automatic compression in action.

```bash
python3 examples/pipeline_demo.py
```

## Project Structure

- `py_context_fs/core.py`: Abstract interfaces and the Router.
- `py_context_fs/pipeline.py`: The Constructor, Loader, and Evaluator.
- `py_context_fs/resolvers.py`: Reference implementations (DictResolver).
