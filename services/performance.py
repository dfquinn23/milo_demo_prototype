# Future: Perf calc, returns, benchmarks, risk stats, attribution


def compute_performance(df):
    """Stub: returns a minimal structure; swap with real logic later."""
    if df is None or getattr(df, "empty", True):
        return {"status": "no_data"}
    return {"status": "ok", "note": "perf stub"}
