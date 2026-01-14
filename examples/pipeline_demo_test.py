from py_context_fs.core import ContextRouter
from py_context_fs.pipeline import ContextConstructor, ContextLoader, ContextEvaluator
from py_context_fs.resolvers import DictResolver


def run_demo() -> None:
    fs = ContextRouter()
    resolver = DictResolver()
    resolver.populate("history/assessment_001.json", {
        "default": "Mathematics " * 200,
        "summary": "Math summary."
    })
    resolver.populate("history/assessment_002.json", {
        "default": '{"topic": "Science", "score": 92}',
        "summary": '{"topic": "Science", "score": 92}'
    })
    fs.mount("/student", resolver)

    constructor = ContextConstructor(fs)
    manifest = constructor.construct(paths=[
        "/student/history/assessment_001.json",
        "/student/history/assessment_002.json",
    ])

    loader = ContextLoader(fs, model="gpt-4")
    context = loader.load(manifest, max_tokens=40)
    assert "(Summary)" in context
    header_tokens = loader.count_tokens(
        "--- File: /student/history/assessment_001.json (Summary) ---\n"
        "Math summary.\n"
    )
    assert header_tokens <= 40

    evaluator = ContextEvaluator(fs)
    agent_output = '{"insight": "Student struggles with fractions."}'
    assert evaluator.evaluate(
        response=agent_output,
        validator=lambda text: text.startswith("{") and text.endswith("}"),
        output_path="/student/profile.json",
    )
    assert fs.open("/student/profile.json").content == agent_output
    print("Pipeline demo test passed.")


if __name__ == "__main__":
    run_demo()
