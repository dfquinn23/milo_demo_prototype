from typing import Dict, Any


class CommsAgent:
    def handle(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Very light demo: pull a recent transcript snippet if available
        transcripts = context.get("transcripts", [])
        snippet = transcripts[-1][:300] + \
            "…" if transcripts else "(no transcripts found)"
        answer = (
            "[CommsAgent STUB] Drafting a concise client communication.\n\n"
            f"Prompt: {prompt}\n\n"
            "Context (latest transcript excerpt):\n"
            f"{snippet}\n\n"
            "Next: plug in tone/style + approval workflow."
        )
        return {"answer": answer, "citations": [], "review_flags": []}
