# crew.py - Orchestration Stub

import os
from typing import Optional, Dict, Any

from agents.comms_agent import CommsAgent
from agents.portfolio_agent import PortfolioAgent
from agents.ips_agent import IPSAgent
from agents.writer_agent import WriterAgent

from services.data_access import load_context_bundle

MODEL_NAME = os.getenv("MODEL_NAME", "stub")
DATA_DIR = os.getenv("DATA_DIR", "./data")


def choose_agent(prompt: str):
    p = prompt.lower()
    if any(k in p for k in ["email", "comms", "communication", "client note"]):
        return CommsAgent()
    if any(k in p for k in ["portfolio", "holdings", "performance", "risk"]):
        return PortfolioAgent()
    if any(k in p for k in ["ips", "policy statement", "guidelines"]):
        return IPSAgent()
    return WriterAgent()


def run_crew(prompt: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Minimal, deterministic stub that:
    1) loads demo context (CSV/YAML/txt) via services,
    2) selects an agent by simple keywording,
    3) returns a structured response.

    Replace internals with real CrewAI orchestration later.
    """

    ctx = load_context_bundle(DATA_DIR)
    agent = choose_agent(prompt)

    draft = agent.handle(prompt=prompt, context=ctx)

    result = {
        "answer": draft["answer"],
        "citations": draft.get("citations", []),
        "review_flags": draft.get("review_flags", []),
        "model": MODEL_NAME,
    }
    return result
