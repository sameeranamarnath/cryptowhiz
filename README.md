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
