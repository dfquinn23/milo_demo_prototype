from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time


from crew import run_crew

app = FastAPI(title="Milo Demo API", version="0.1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        # Add your deployed Streamlit origin(s) here, e.g.:
        # "https://milo-demo.streamlit.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = None


class GenerateResponse(BaseModel):
    answer: str
    citations: List[str] = []
    review_flags: List[str] = []
    model: str = "stub"
    latency_ms: int = 0


@app.get("/health")
def health():
    return {"status": "ok", "service": "milo-demo-api"}


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    t0 = time.perf_counter()
    # call orchestration sub
    result = run_crew(prompt=req.prompt, session_id=req.session_id)

    latency_ms = int((time.perf_counter() - t0) * 1000)
    return GenerateResponse(
        answer=result.get("answer", ""),
        citations=result.get("citations", []),
        review_flags=result.get("review_flags", []),
        model=result.get("model", "stub"),
        latency_ms=latency_ms,
    )
