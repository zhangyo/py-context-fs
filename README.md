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
- **`ContextRouter`**: The router that mounts sources at paths (e.g., `/student`, `/db`).
- **`ContextSource`**: Abstract adapter for data sources. Implement this to connect to SQL, Vector DBs, or APIs.
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

## Implementing a Context Engineering Pipeline

This repository provides the building blocks to implement a full context engineering pipeline that separates data access (VFS) from context management (Pipeline). The pipeline is composed of three primary components that map to the Agentic File System pattern.

### Context Constructor (Selection and Compression)
The Constructor is responsible for assembling the necessary context for a specific reasoning task. In the iClass-style architecture, the Constructor uses the VFS to browse the student's history rather than dumping the entire database into the prompt. For example, it might traverse the `/history` directory and filter for assessments tagged with "Mathematics" within the last 30 days. It relies on VFS metadata (file size, modification date, tags) to rank and select the most relevant files. If a resolver exposes multiple views, the Constructor can prioritize compressed views as part of the selection strategy.

In `py-context-fs`, this is modeled via `SelectionCriteria`, which supports metadata filters, regex include/exclude patterns, ranking, and optional pre-budgeting based on estimated token counts. This allows the Constructor to produce a prioritized `ContextManifest` that the Loader can refine under a strict budget.

SelectionCriteria fields:
- `query`: Search query against the VFS.
- `paths`: Explicit paths to include.
- `include_patterns`: Regex patterns to include (path-based).
- `exclude_patterns`: Regex patterns to exclude (path-based).
- `metadata_filter`: Predicate to filter using metadata.
- `ranker`: Function to assign a priority score for ranking.
- `max_results`: Limit number of selected files.
- `max_tokens`: Optional pre-budget cap (approximate, summary-first).
- `token_counter`: Optional function to estimate token cost (summary-first).
- `preferred_view`: Preferred view (e.g., `summary`).
- `view_selector`: Function to pick a view based on metadata.

### Context Loader (Delivery and Streaming)
The Loader manages the constraints of the Foundation Model, specifically the token window. It takes the `ContextManifest` produced by the Constructor and streams those files into the agent's context. The Loader counts tokens for each file and enforces the budget (for example, 128k tokens). When a selection exceeds the limit, it requests compressed views from the VFS (for example, reading `transcript.summary.md` instead of `transcript.detailed.md`). This ensures the agent always receives a coherent, bounded set of information without manual curation. Use `load_stream()` when you want incremental delivery or early aborts, and `load()` when you want a single string.

### Context Evaluator (Validation and Persistence)
The Evaluator closes the loop. After the agent generates a response or a new insight (for example, "Student struggles with equivalent fractions"), the Evaluator validates the output against ground truth (rubrics stored in `/system/rubrics/`). It is also responsible for write-back. Once validated, it writes the insight to the student's profile file (for example, `/students/123/profile.md`). A resolver can intercept that write and persist it to durable storage such as Postgres, ensuring the system learns and evolves over time.

The Evaluator accepts optional audit metadata (validator name, evidence paths, timestamps) to support traceability and compliance.

### Sample Test Code (Constructor, Loader, Evaluator)
This self-contained snippet demonstrates the three components working together using the in-memory `DictResolver`.

```python
from py_context_fs.core import ContextRouter
from py_context_fs.pipeline import (
    ContextConstructor,
    ContextLoader,
    ContextEvaluator,
    SelectionCriteria,
)
from py_context_fs.resolvers import DictResolver

def is_valid_json(text: str) -> bool:
    return text.strip().startswith("{") and text.strip().endswith("}")

fs = ContextRouter()
resolver = DictResolver()
resolver.populate("history/assessment_001.json", {
    "default": '{"topic": "Mathematics", "score": 78, "date": "2025-01-10"}',
    "summary": '{"topic": "Mathematics", "score": 78}'
})
resolver.populate("history/assessment_002.json", {
    "default": '{"topic": "Science", "score": 92, "date": "2025-01-05"}',
    "summary": '{"topic": "Science", "score": 92}'
})
fs.mount("/student", resolver)

# 1) Constructor: select relevant files (explicit paths or search-based)
constructor = ContextConstructor(fs)
manifest = constructor.construct(
    criteria=SelectionCriteria(
        paths=[
            "/student/history/assessment_001.json",
            "/student/history/assessment_002.json",
        ],
        preferred_view="summary",
    )
)

# 2) Loader: enforce token budget and fall back to summary views
loader = ContextLoader(fs, model="gpt-4")
context = loader.load(manifest, max_tokens=40)
print(context)

# 3) Evaluator: validate and persist agent output
evaluator = ContextEvaluator(fs)
agent_output = '{"insight": "Student struggles with equivalent fractions."}'
evaluator.evaluate(
    response=agent_output,
    validator=is_valid_json,
    output_path="/student/profile.json",
    validator_name="json_shape_v1",
    evidence_paths=["/student/history/assessment_001.json"],
)
print(fs.open("/student/profile.json").content)
```

## Usage

### Basic File System Operations

```python
from py_context_fs.core import ContextRouter
from py_context_fs.resolvers import DictResolver

# 1. Initialize FS
fs = ContextRouter()

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
from py_context_fs.pipeline import ContextConstructor, ContextLoader, SelectionCriteria

# 1. Selection (Stage A)
constructor = ContextConstructor(fs)
manifest = constructor.construct(
    criteria=SelectionCriteria(
        query="Mathematics",
        include_patterns=[r"history/.*\\.json$"],
        metadata_filter=lambda meta: meta.get("days_ago", 999) <= 30,
        ranker=lambda path, meta: float(meta.get("priority", 0)),
        max_results=25,
        max_tokens=4000,
        preferred_view="summary",
    )
)

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
from py_context_fs.core import ContextSource, ContextFile

class DatabaseResolver(ContextSource):
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
- `py_context_fs/repository.py`: Persistent history/memory/scratchpad repository.

## Persistent Context Repository

The repository provides durable history, memory, and scratchpad layers with simple lifecycle transitions.

```python
from py_context_fs.repository import PersistentContextRepository

repo = PersistentContextRepository("./context_repo")

# History append (immutable log)
history_path = repo.append_history("Raw interaction text", metadata={"actor": "user"})

# Scratchpad write
scratch_path = repo.persist_scratchpad("Draft reasoning")

# Promote scratchpad -> history
repo.commit_scratchpad_to_history(scratch_path, metadata={"reviewed": True})

# Promote history -> memory (optionally transform)
repo.promote_history_to_memory(history_path, memory_key="session_001")
```
