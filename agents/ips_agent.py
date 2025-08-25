from typing import Dict, Any


class IPSAgent:
    def handle(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        ips = context.get("ips", {})
        policy_keys = ", ".join(sorted(ips.keys())) if isinstance(
            ips, dict) else "(no ips.yaml)"
        answer = (
            "[IPSAgent STUB] Evaluating against policy guidance.\n\n"
            f"Prompt: {prompt}\n\n"
            f"IPS sections found: {policy_keys}\n\n"
            "Next: wire compliance checks from services."
        )
        return {"answer": answer, "citations": [], "review_flags": []}
