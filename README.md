# cryptowhiz

A screener for high-momentum crypto setups. It pulls coins from CoinMarketCap and
CoinGecko, filters them on volume and 24h move, plots price charts, and asks an
LLM for a read on each candidate.

## What it does

- Pulls the top coins from CoinMarketCap and CoinGecko, with an on-disk cache
  (`cache/`) so repeated runs do not burn API quota
- Filters on a volume floor and a 24h change band (`filter_cryptos`)
- Saves OHLCV charts as `<symbol>_chart.png` (CoinMarketCap and CoinGecko paths)
- Asks Azure OpenAI for a short analysis of each filtered coin

Results land in `crypto_screener.json` / `crypto_screener.txt`.

## Stack

- Python, pandas, matplotlib
- CoinMarketCap and CoinGecko APIs
- Azure OpenAI for the commentary
- `ratelimit` / `backoff` to stay inside free API tiers

## Setup

```
pip install -r requirements.txt
```

Create `.env` (or export) with:

```
CMC_API_KEY=your-coinmarketcap-key
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

## Run

```
python cryptowiz.py
```

## Notes

- Screening output is not investment advice; the filters are deliberately crude.
- Credentials come from the environment - nothing is hardcoded.

## Research service (`ai/`)

`cryptowiz.py` screens and charts. `ai/` adds a LangGraph research graph that
splits the analysis across nodes and fans them back in:

```
START -> fetch_market -+-> technicals -+
                       |               +-> risk -> report -> END
                       +-> news ------ +
```

- **Numbers stay deterministic** - RSI-14, SMA-50/200 and annualised volatility are computed in pandas, not by a model
- **Retrieval** - stored headlines and notes are searched in Qdrant per symbol
- **Risk node** - has to reconcile momentum, volatility and news, and name what would invalidate the thesis
- **Models** - vLLM (`Qwen/Qwen3-32B` chat, `BAAI/bge-m3` embeddings)

```
docker compose -f docker-compose.ai.yml up
```

`POST /notes` stores headlines, `POST /analyse` runs the graph, and
`POST /analyse/stream` streams it. See [`ai/README.md`](ai/README.md).
