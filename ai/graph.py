"""Multi-agent research graph for one crypto symbol.

    START -> fetch_market -+-> technicals -+
                           |               +-> risk -> report -> END
                           +-> news ------ +

`technicals` is deterministic pandas - no model touches the numbers. The model
only writes prose, and only after it has been handed the computed values.
"""

from typing import Any, TypedDict

import httpx
import pandas as pd
from langgraph.graph import END, START, StateGraph

from core import chat_model, get_settings, search_notes


class ResearchState(TypedDict, total=False):
    symbol: str
    days: int
    candles: list[dict[str, Any]]
    market: dict[str, Any]
    indicators: dict[str, Any]
    news: list[dict[str, Any]]
    risk: str
    report: str


def fetch_market(state: ResearchState) -> dict[str, Any]:
    s = get_settings()
    coin = state["symbol"].lower()
    days = state.get("days") or s.candles_days
    with httpx.Client(timeout=30) as client:
        chart = client.get(
            f"{s.coingecko_base}/coins/{coin}/market_chart",
            params={"vs_currency": "usd", "days": days, "interval": "daily"},
        ).json()
        stats = client.get(
            f"{s.coingecko_base}/coins/markets",
            params={"vs_currency": "usd", "ids": coin},
        ).json()
    candles = [{"t": p[0], "close": p[1]} for p in chart.get("prices", [])]
    return {"candles": candles, "market": stats[0] if stats else {}, "days": days}


def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, 1e-10)
    return 100 - (100 / (1 + rs))


def technicals(state: ResearchState) -> dict[str, Any]:
    df = pd.DataFrame(state.get("candles", []))
    if df.empty or len(df) < 30:
        return {"indicators": {"error": "not enough candles for indicators"}}
    close = df["close"].astype(float)
    returns = close.pct_change().dropna()
    indicators = {
        "last_close": round(float(close.iloc[-1]), 4),
        "rsi14": round(float(_rsi(close).iloc[-1]), 2),
        "sma50": round(float(close.rolling(50).mean().iloc[-1]), 4) if len(close) >= 50 else None,
        "sma200": round(float(close.rolling(200).mean().iloc[-1]), 4) if len(close) >= 200 else None,
        "annualised_vol": round(float(returns.std() * (365 ** 0.5)), 4),
        "pct_change_30d": (
            round(float(close.iloc[-1] / close.iloc[-31] - 1) * 100, 2) if len(close) > 31 else None
        ),
    }
    return {"indicators": indicators}


def news(state: ResearchState) -> dict[str, Any]:
    return {"news": search_notes(f"{state['symbol']} outlook", state["symbol"].lower())}


def risk(state: ResearchState) -> dict[str, Any]:
    headlines = "\n".join(f"- {n.get('text', '')[:200]}" for n in state.get("news", [])) or "- (none stored)"
    prompt = (
        "You are the risk node in a research pipeline. Using the numbers and notes "
        "below, state the case for and against, and name what would invalidate it. "
        "Do not invent figures.\n\n"
        f"Symbol: {state['symbol']}\nIndicators: {state.get('indicators', {})}\n"
        f"Market: {state.get('market', {})}\nNotes:\n{headlines}"
    )
    return {"risk": str(chat_model().invoke(prompt).content).strip()}


def report(state: ResearchState) -> dict[str, Any]:
    prompt = (
        "Write a short research note (max 200 words) for a trading desk. Lead with "
        "the conclusion, then the support, then the main risk. Include the numbers.\n\n"
        f"Symbol: {state['symbol']}\nIndicators: {state.get('indicators', {})}\n"
        f"Risk view:\n{state.get('risk', '')}"
    )
    return {"report": str(chat_model().invoke(prompt).content).strip()}


def build_graph():
    g = StateGraph(ResearchState)
    g.add_node("fetch_market", fetch_market)
    g.add_node("technicals", technicals)
    g.add_node("news", news)
    g.add_node("risk", risk)
    g.add_node("report", report)

    g.add_edge(START, "fetch_market")
    # fan out
    g.add_edge("fetch_market", "technicals")
    g.add_edge("fetch_market", "news")
    # fan in
    g.add_edge("technicals", "risk")
    g.add_edge("news", "risk")
    g.add_edge("risk", "report")
    g.add_edge("report", END)
    return g.compile()


APP = build_graph()


def analyse(symbol: str, days: int | None = None) -> ResearchState:
    return APP.invoke({"symbol": symbol.lower(), "days": days or get_settings().candles_days})
