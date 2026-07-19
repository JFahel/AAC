from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(
    title="Task Tracker API",
    description="A minimal learning-project REST API for tracking tasks.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict:
    """Return service health status and the current UTC timestamp."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
