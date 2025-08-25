from typing import Dict, Any
import pandas as pd


class PortfolioAgent:
    def handle(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        df = context.get("portfolio")
        summary = "(no portfolio.csv loaded)"
        if isinstance(df, pd.DataFrame) and not df.empty:
            cols = ", ".join(df.columns[:8])
            summary = f"Rows: {len(df)}, Cols: {len(df.columns)} — Preview cols: {cols}"
        answer = (
            "[PortfolioAgent STUB] Providing a quick portfolio summary.\n\n"
            f"Prompt: {prompt}\n\n"
            f"Portfolio summary: {summary}\n\n"
            "Next: compute perf, risk, attribution via services."
        )
        return {"answer": answer, "citations": [], "review_flags": []}
