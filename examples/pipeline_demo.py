import sys
import os
import shutil

# Ensure the package is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from py_context_fs.core import ContextRouter
from py_context_fs.repository import PersistentContextRepository
from py_context_fs.resolvers import DictResolver
from py_context_fs.pipeline import ContextConstructor, ContextLoader, ContextEvaluator

def main():
    print("Initializing Agentic File System...")
    fs = ContextRouter()

    # 0. Setup persistent repository (history/memory/scratchpad)
    repo_root = os.path.join(os.path.dirname(__file__), "context_repo")
    repo = PersistentContextRepository(repo_root)
    history_path = repo.append_history("Student asked about AFS patterns.", metadata={"actor": "user"})
    repo.promote_history_to_memory(history_path, memory_key="session_001")
    fs.mount("/context", repo)
    
    # 1. Setup Resolver with Mock Data
    student_resolver = DictResolver()
    
    long_transcript = "This is a very long transcript of a lecture " * 100
    short_summary = "Lecture covered: Basics of AFS."
    
    student_resolver.populate("transcript.txt", {
        "default": long_transcript,
        "summary": short_summary
    })
    
    student_resolver.populate("syllabus.txt", {
        "default": "Module 1: Intro\nModule 2: Advanced",
        "summary": "M1, M2"
    })

    # Mount the resolver
    fs.mount("/student", student_resolver)
    print("Mounted DictResolver at /student")

    # 2. Pipeline Stage A: Constructor
    print("\n--- Stage A: Constructor ---")
    constructor = ContextConstructor(fs)
    # Let's say we want everything in /student
    # In a real scenario, we might use search or specific selection logic
    # Here let's manually pick detailed files
    manifest = constructor.construct(
        paths=[
            "/student/transcript.txt",
            "/student/syllabus.txt",
            "/context/memory/session_001.json",
        ]
    )
    print(f"Manifest created with files: {manifest.files}")

    # 3. Pipeline Stage B: Loader (with strict token limit)
    print("\n--- Stage B: Loader ---")
    loader = ContextLoader(fs)
    
    # Set a small limit to force compression/skipping
    # "This is a very long transcript..." is 8 tokens roughly. 100 times is 800 tokens.
    # Syllabus is small.
    # Let's set limit to 200 tokens. This should force transcript to use summary.
    max_tokens = 200
    print(f"Loading context with max_tokens={max_tokens}...")
    
    context_chunks = []
    for chunk in loader.load_stream(manifest, max_tokens=max_tokens):
        context_chunks.append(chunk)
        if "syllabus.txt" in chunk:
            print("Early abort triggered after syllabus chunk.")
            break
    context = "\n".join(context_chunks)
    
    print("\n[Generated Context START]")
    for chunk in context_chunks:
        print(chunk)
    print("[Generated Context END]")

    # Check expectations
    if "Lecture covered: Basics of AFS" in context and "This is a very long transcript" not in context:
        print("\nSUCCESS: Transcript fell back to summary views as expected.")
    elif "This is a very long transcript" in context:
        print("\nWARNING: Transcript was loaded in full (maybe token count logic differs or limit too high).")
    else:
        print("\nFAILURE: Transcript context missing entirely.")

    # 4. Pipeline Stage C: Evaluator
    print("\n--- Stage C: Evaluator ---")
    evaluator = ContextEvaluator(fs)
    
    # Mock LLM response
    mock_llm_response = '{"grade": "A", "comments": "Good job"}'
    
    def json_validator(text):
        return text.startswith("{") and text.endswith("}")

    saved = evaluator.evaluate(
        mock_llm_response,
        json_validator,
        "/student/grade.json",
        validator_name="json_shape_v1",
        history_paths=[f"/context/{history_path}"],
        decision_metadata={"run_id": "demo-001"},
    )
    if saved:
        print("Response validated and saved to /student/grade.json")
        saved_file = fs.open("/student/grade.json")
        print(f"Read back saved file: {saved_file.content}")
    else:
        print("Response validation failed.")

    # Cleanup repository created for demo runs
    shutil.rmtree(repo_root, ignore_errors=True)

if __name__ == "__main__":
    main()
