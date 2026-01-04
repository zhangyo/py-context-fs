**Role:**
You are a Principal Software Architect specializing in Python and Generative AI Infrastructure.

**Goal:**
Create the foundational code for a new open-source Python library named **`py-context-fs`**.
This library implements the **Agentic File System (AFS)** pattern and the **Context Engineering Pipeline** as described in the research paper *"Everything is Context"*.

The research paper *"Everything is Context"* is available at: `docs/2512.05470v1.pdf`.

You can also take a look at the `aigne-framework` for a reference implementation in TypeScript: [https://github.com/AIGNE-io/aigne-framework/tree/main/afs](https://github.com/AIGNE-io/aigne-framework/tree/main/afs)

**Core Concept:**
The library separates **Data Access** (handled by the VFS) from **Context Management** (handled by the Pipeline).

1. **The VFS** treats all data (DBs, APIs, Memory) as "Virtual Files".
2. **The Pipeline** (Constructor, Loader, Evaluator) governs how these files are selected, compressed, and loaded into the LLM's limited token window.

---

### **Technical Requirements & Specifications**

#### **1. Core VFS Module (`py_context_fs.core`)**

Define the abstract interfaces that allow Agents to interact with data.

* **`ContextNode` (Abstract Base Class):**
    * `read(path: str, view: str = "default") -> ContextFile`: Returns a dataclass containing `content` (str), `metadata` (dict), and `token_count` (int, optional). Note the `view` parameter (critical for compression strategies).
    * `list(path: str) -> List[str]`: Lists "files" in this node.
    * `search(query: str) -> List[str]`: Returns paths matching the query.
    * `write(path: str, content: str, metadata: dict = None) -> None`: Persists state.

* **`ContextFS` (The Router):**
    * `mount(path_prefix: str, node: ContextNode)`: Registers a resolver.
    * `open(path: str, view: str = "default") -> ContextFile`: Routes to the correct node.
    * `exists(path: str) -> bool`.

#### **2. The Pipeline Module (`py_context_fs.pipeline`)**

Implement the three-stage pipeline logic provided in the specs.

* **Component A: `ContextConstructor`**
    * **Role:** Selection.
    * **Input:** A `ContextFS` instance and a `SelectionCriteria` (e.g., regex patterns, list of required paths, or a search query).
    * **Output:** A `ContextManifest` (an ordered list of files to *attempt* to load, ranked by priority).
    * **Logic:** It should traverse the VFS (using `list` or `search`) to find relevant virtual files and add them to the manifest.

* **Component B: `ContextLoader`**
    * **Role:** Token Budgeting & Streaming.
    * **Dependencies:** Use `tiktoken` for accurate counting.
    * **Configuration:** Accepts `max_tokens` (e.g., 8000).
    * **Logic (The "Knapsack" Algorithm):**
        1. Iterate through the `ContextManifest`.
        2. For each file, calculate `tokens = count(file.content)`.
        3. **Check:** `if current_total + tokens < max_tokens`:
            * Add file to the final Context Object.
        4. **Compression Strategy:**
            * `else`: Attempt to request a smaller "view" from the VFS (e.g., call `fs.open(path, view="summary")`).
            * If the "summary" view fits, add it. If not, skip or truncate (configurable).
    * **Output:** The final string or message list ready for the LLM.

* **Component C: `ContextEvaluator`**
    * **Role:** Validation & Persistence.
    * **Logic:** A wrapper that takes the LLM's response, validates it (e.g., JSON schema check), and calls `fs.write()` to save the result back to a "Memory" mount point (e.g., `/memory/latest_run.json`).

#### **3. Standard Resolvers (`py_context_fs.resolvers`)**

* **`DictResolver`:** An in-memory implementation of `ContextNode` using a Python dictionary. Useful for testing.
* **`ReadOnlyWrapper`:** A decorator/proxy that raises permission errors on `write()`.

---

### **Deliverables**

Please provide the code for the following structure:

1. `py_context_fs/core.py`: The interfaces and `ContextFS` router.
2. `py_context_fs/pipeline.py`: The `Constructor`, `Loader` (with `tiktoken`), and `Evaluator`.
3. `examples/pipeline_demo.py`: A script demonstrating:
    * Mounting a `DictResolver` at `/student`.
    * Populating it with a long "transcript" and a short "summary".
    * Running the **Loader** with a strict token limit to demonstrate it automatically falling back to the "summary" view when the full transcript is too large.

**Constraints:**

* Use Python 3.10+ (Type hints, Dataclasses).
* Docstrings must follow Google Style.
* Keep the design extensible (users will implement SQL/Vector resolvers later).