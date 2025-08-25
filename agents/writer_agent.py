from typing import Dict, Any


class WriterAgent:
    def handle(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        answer = (
            "[WriterAgent STUB] General drafting agent.\n\n"
            f"Prompt: {prompt}\n\n"
            "Next: plug in retrieval + drafting model."
        )
        return {"answer": answer, "citations": [], "review_flags": []}
