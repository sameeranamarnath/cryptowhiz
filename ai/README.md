# Crypto research service

A multi-agent layer over the screener. Rather than one prompt asking a model to
"analyse this coin", the work is split across nodes that each own one question,
then a risk node that has to reconcile them.

## Graph

```
START -> fetch_market -+-> technicals -+
                       |               +-> risk -> report -> END
                       +-> news ------ +
```

| Node | What it does |
| --- | --- |
| `fetch_market` | pulls candles and 24h stats from CoinGecko |
| `technicals` | computes RSI-14, SMA-50/200 and realised volatility - plain pandas, no model |
| `news` | Qdrant retrieval over stored headlines/notes for the symbol |
| `risk` | weighs momentum against volatility and news; states what would invalidate the thesis |
| `report` | joins everything into one readable note with the numbers attached |

`technicals` and `news` run in parallel off `fetch_market`, then fan in to `risk`.

## Stack

- LangGraph for the fan-out/fan-in graph
- vLLM serving `Qwen/Qwen3-32B` (chat) and `BAAI/bge-m3` (embeddings)
- Qdrant for news/notes retrieval
- CoinGecko for market data, pandas for indicators
- FastAPI + SSE

## Run

```
docker compose -f ../docker-compose.ai.yml up
```

```
curl -X POST localhost:8080/analyse -H 'content-type: application/json' \
  -d '{"symbol": "bitcoin", "days": 180}'
```

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | liveness and resolved model names |
| `POST` | `/notes` | store headlines/notes for retrieval |
| `POST` | `/analyse` | run the graph for one symbol |
| `POST` | `/analyse/stream` | same, as SSE per graph node |
| `GET` | `/search?q=` | retrieval-only debug view |

## Note

Nothing here is investment advice, and the indicators are the obvious ones on
purpose - the interesting part is the graph shape and the retrieval, not the
signal quality. vLLM wants a GPU; set `LLM_BASE_URL` to a hosted endpoint otherwise.
