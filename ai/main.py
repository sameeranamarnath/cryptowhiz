"""HTTP surface for the crypto research service."""

import json
from collections.abc import AsyncIterator
from typing import Any

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from core import get_settings, search_notes, upsert_notes
from graph import APP, analyse
from guardrails import sanitise

api = FastAPI(title="crypto research graph", version="1.0.0")


class Note(BaseModel):
    text: str = Field(min_length=5)
    symbol: str | None = None
    source: str | None = None


class NotesRequest(BaseModel):
    notes: list[Note]


class AnalyseRequest(BaseModel):
    symbol: str = Field(min_length=2, max_length=40)
    days: int | None = None


@api.get("/health")
def health() -> dict[str, Any]:
    s = get_settings()
    return {
        "status": "ok",
        "llm_model": s.llm_model,
        "embed_model": s.embed_model,
        "collection": s.qdrant_collection,
    }


@api.post("/notes")
def add_notes(req: NotesRequest) -> dict[str, int]:
    payload = [
        {**{k: v for k, v in n.model_dump().items() if v is not None}, "text": sanitise(n.text)}
        for n in req.notes
    ]
    return {"stored": upsert_notes(payload)}


@api.post("/analyse")
def analyse_endpoint(req: AnalyseRequest) -> dict[str, Any]:
    result = analyse(req.symbol, req.days)
    return {
        "symbol": result.get("symbol"),
        "indicators": result.get("indicators", {}),
        "risk": result.get("risk", ""),
        "report": result.get("report", ""),
        "notes_used": len(result.get("news", [])),
    }


@api.post("/analyse/stream")
async def analyse_stream(req: AnalyseRequest) -> StreamingResponse:
    async def events() -> AsyncIterator[str]:
        state: dict[str, Any] = {"symbol": req.symbol.lower()}
        if req.days:
            state["days"] = req.days
        for step in APP.stream(state):
            for node, update in step.items():
                payload = json.dumps({"node": node, "update": _safe(update)})
                yield f"event: node\ndata: {payload}\n\n"
                state.update(update)
        yield f"event: done\ndata: {json.dumps(_safe(state))}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream")


def _safe(d: dict[str, Any]) -> dict[str, Any]:
    """Candle arrays are large and useless to a UI; drop them from the stream."""
    return {k: v for k, v in d.items() if k not in {"candles", "market"}}


@api.get("/search")
def quick_search(q: str, symbol: str | None = None) -> dict[str, Any]:
    return {"hits": search_notes(q, symbol)}
