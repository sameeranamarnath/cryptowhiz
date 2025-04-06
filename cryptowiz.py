'''
Alright, I hear you loud and clear! You're looking for those juicy, high-return crypto plays. While identifying positions with 30-100% daily moves or 300% over several months is ambitious (and definitely possible in the crypto world), it also comes with big risks. So, let’s approach this systematically and responsibly.   
  
Here’s the kind of data I’d need to help you screen and analyze cryptos for such setups:  
   
---  
   
### **1. Market Conditions**  
   - **Overall Market Sentiment:** Is Bitcoin (BTC) and Ethereum (ETH) bullish or bearish? The crypto market often follows BTC, so understanding its trend is crucial.  
   - **Dominance:** Bitcoin Dominance (BTC.D) can help determine whether altcoins are likely to rally. Lower dominance often signals an altcoin season.  
   
---  
   
### **2. Specific Coin Data**  
   - **Market Cap:** Are you looking for small-cap, mid-cap, or large-cap cryptos? Smaller-cap coins tend to have higher potential returns but also higher risk.  
   - **Circulating Supply vs. Total Supply:** Coins with a small circulating supply and low inflation can pump harder.  
   - **Volume:** High volume is essential for liquidity and to confirm strong moves. Coins with low volume are risky because it's harder to enter and exit positions.  
   
---  
   
### **3. Technical Analysis (TA)**  
   - **Price Action:** Look for coins forming bullish patterns like breakouts, consolidation, or support levels. Are they showing signs of accumulation?  
   - **Momentum Indicators:** RSI, MACD, and Stochastic Oscillator can help identify overbought or oversold conditions.  
   - **Key Levels:** Support and resistance zones, Fibonacci retracement levels, or moving averages like the 50-day and 200-day can act as triggers.  
   - **Volume Profile:** Check for volume spikes on breakouts—this is crucial to confirm the strength of the move.  
   
---  
   
### **4. Fundamental Catalysts**  
   - **Upcoming News:** Look for tokens with upcoming events like partnerships, mainnet launches, or protocol upgrades. Websites like CoinMarketCal track crypto events.  
   - **Use Case:** Does the project solve a real problem? Meme coins can pump, but fundamentally strong projects have better long-term potential.  
   - **Ecosystem Growth:** Are they onboarding developers, partnerships, or new integrations? For example, Layer 2 projects like Arbitrum or Optimism have been gaining traction.  
   
---  
   
### **5. Sentiment Analysis**  
   - **Social Media Hype:** Monitor platforms like Twitter, Reddit, and Telegram for trending coins. But beware of pump-and-dump schemes.  
   - **Fear & Greed Index:** This can help gauge whether the market is overly bullish or fearful—use it to time your entries.  
   
---  
   
### **6. Time Horizon**  
   - **Day Trades (30-100% Daily Moves):** Focus on highly volatile coins with small market caps and high volume. Look for coins breaking out of patterns or showing explosive momentum.  
   - **Swing Trades (300% in 8 Months):** Look for fundamentally strong mid-cap coins that are undervalued or in accumulation phases.  
   
---  
   
### **What I Need from You:**  
1. **Risk Tolerance:** Are you comfortable with high-risk, high-reward plays, or do you want a mix of safer options?  
2. **Capital Allocation:** How much are you planning to allocate to these trades? This will help with position sizing.  
3. **Preferred Type of Crypto:** Are you looking at meme coins, DeFi projects, gaming tokens, or infrastructure plays?  
4. **Time Availability:** Are you actively monitoring the markets, or do you want more set-it-and-forget-it setups?  
   
---  
   
### **Tools for Screening**  
If you’re ready to start screening, here are some tools I recommend:  
- **CoinMarketCap/CoinGecko:** For market data and trending coins.  

'''  
import requests  
import pandas as pd  
from openai import AzureOpenAI  
# Azure OpenAI API Config  
AZURE_OPENAI_ENDPOINT = "https://samee-m94pw60g-eastus2.openai.azure.com/"  
AZURE_OPENAI_API_KEY = "BO8xRWdpmbIkArN0eNGZa0Dth49ss0LWC4Hhv86JqYZUAetbYfMcJQQJ99BDACHYHv6XJ3w3AAAAACOG45gu"  
AZURE_OPENAI_DEPLOYMENT = "gpt-4.5-preview"  # e.g., "gpt-4" or "gpt-3.5-turbo"  
  
import requests  
import matplotlib.pyplot as plt  
from datetime import datetime, timedelta  
import os  
#from dotenv import load_dotenv  
  
# Load your CoinMarketCap API key from a .env file or environment variable  
#load_dotenv()  
CMC_API_KEY = "24e7dbc7-b1e3-49c0-8e80-79d787f829f5"  
  
def get_crypto_historical_chart(symbol, days=7, interval='daily', currency='USD'):  
    """  
    Fetch historical OHLCV data from CoinMarketCap and plot a price chart.  
  
    Parameters:  
    - symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')  
    - days: Number of days in the past to retrieve data  
    - interval: 'daily' or 'hourly'  
    - currency: Quote currency (default USD)  
  
    Saves a chart image as '{symbol}_chart.png'  
    """  
    # API Endpoint  
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical"  
  
    # Calculate date range  
    end_date = datetime.utcnow()  
    start_date = end_date - timedelta(days=days)  
  
    # Format dates to ISO 8601  
    time_start = start_date.strftime('%Y-%m-%dT%H:%M:%S')  
    time_end = end_date.strftime('%Y-%m-%dT%H:%M:%S')  
  
    # API request headers  
    headers = {  
        'Accepts': 'application/json',  
        'X-CMC_PRO_API_KEY': CMC_API_KEY,  
    }  
  
    # Request parameters  
    params = {  
        'symbol': symbol,  
        'time_start': time_start,  
        'time_end': time_end,  
        'interval': interval,  
        'convert': currency  
    }  
  
    # API request  
    response = requests.get(url, headers=headers, params=params)  
      
    if response.status_code != 200:  
        print(f"Error fetching data: {response.status_code}, {response.text}")  
        return  
  
    data = response.json()  
    if 'data' not in data or 'quotes' not in data['data']:  
        print("No data returned from API.")  
        return  
  
    quotes = data['data']['quotes']  
  
    # Extract timestamps and closing prices  
    dates = [datetime.strptime(q['time_close'][:10], '%Y-%m-%d') for q in quotes]  
    closes = [q['quote'][currency]['close'] for q in quotes]  
  
    # Plotting the chart  
    plt.figure(figsize=(10, 5))  
    plt.plot(dates, closes, marker='o', linestyle='-', color='blue')  
    plt.title(f'{symbol} Historical Prices ({interval.capitalize()})')  
    plt.xlabel('Date')  
    plt.ylabel(f'Price ({currency})')  
    plt.grid(True)  
    plt.xticks(rotation=45)  
    plt.tight_layout()  
  
    # Save plot as image  
    filename = f'{symbol}_chart.png'  
    plt.savefig(filename)  
    plt.close()  
    print(f"Chart saved as {filename}")  
  

# Example usage:  
#get_crypto_historical_chart('BTC', days=30, interval='daily')    

import requests  
import matplotlib.pyplot as plt  
from datetime import datetime  
  
def get_crypto_historical_chart_coingecko(coin_id, days=7, currency='usd'):  
    """  
    Fetch historical price data from CoinGecko and plot a price chart.  
  
    Parameters:  
    - coin_id: CoinGecko coin ID (e.g., 'bitcoin', 'ethereum')  
    - days: Number of past days to retrieve data ('1', '7', '14', '30', '90', '180', '365', 'max')  
    - currency: Quote currency (default 'usd')  
  
    Saves a chart image as '{coin_id}_chart.png'  
    """  
    # API endpoint  
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'  
  
    # Request parameters  
    params = {  
        'vs_currency': currency,  
        'days': days,  
        'interval': 'daily' if int(days) >= 2 else 'hourly'  
    }  
  
    # API request  
    response = requests.get(url, params=params)  
  
    if response.status_code != 200:  
        print(f"Error fetching data: {response.status_code}, {response.text}")  
        return  
  
    data = response.json()  
  
    if 'prices' not in data:  
        print("No price data returned from API.")  
        return  
  
    # Extract timestamps and prices  
    timestamps = [price_point[0] for price_point in data['prices']]  
    prices = [price_point[1] for price_point in data['prices']]  
  
    # Convert timestamps from milliseconds to datetime  
    dates = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]  
  
    # Plotting the chart  
    plt.figure(figsize=(10, 5))  
    plt.plot(dates, prices, marker='o', linestyle='-', color='green')  
    plt.title(f'{coin_id.capitalize()} Historical Prices (Last {days} days)')  
    plt.xlabel('Date')  
    plt.ylabel(f'Price ({currency.upper()})')  
    plt.grid(True)  
    plt.xticks(rotation=45)  
    plt.tight_layout()  
  
    # Save plot as image  
    filename = f'{coin_id}_chart.png'  
    plt.savefig(filename)  
    plt.close()  
    print(f"Chart saved as {filename}")  
  
# Example usage:  
# coin_id examples: 'bitcoin', 'ethereum', 'cardano', etc.  
#get_crypto_historical_chart_coingecko('bitcoin', days=30, currency='usd')  
#get_crypto_historical_chart_coingecko('ethereum', days=180, currency='usd')  
#get_crypto_historical_chart_coingecko('XRP', days=180, currency='usd')  

def filter_cryptos(df, min_volume=500000, min_change=10, max_change=1000, max_market_cap=None):  
    filtered = df[  
        (df['24h_volume'] >= min_volume) &  # Minimum 24-hour trading volume  
        (df['24h_change_%'] >= min_change) &  # Minimum % change  
        (df['24h_change_%'] <= max_change)   # Maximum % change  
    ]  
      
    if max_market_cap:  
        filtered = filtered[filtered['market_cap'] <= max_market_cap]  
      
    return filtered  
  
  
# Function to interact with Azure OpenAI and get advice  
import openai  
endpoint = "https://samee-m94pw60g-eastus2.openai.azure.com/"
model_name = "gpt-4.5-preview"
deployment = "gpt-4.5-preview"

subscription_key = AZURE_OPENAI_API_KEY
api_version = "2024-12-01-preview"

  
def get_openai_advice(symbol, name, price, change, volume, market_cap):  
    # Print the input data for debugging  
    print(f"Fetching advice for: Symbol={symbol}, Name={name}, Price={price}, Change={change}, Volume={volume}, Market Cap={market_cap}")  
  
    # Handle missing names  
    name = name if name else "Unknown"  
  
    # Construct the prompt  
    prompt = f"""  
    Based on the following crypto data:  
    - Symbol: {symbol}  
    - Name: {name}  
    - Price: ${price}  
    - 24-hour Change: {change}%  
    - 24-hour Volume: ${volume}  
    - Market Cap: ${market_cap}  
      
    Provide a detailed analysis and actionable advice for this cryptocurrency. Consider factors such as market cap size, trading volume, price change momentum, and potential risks. Provide the best suggestions for day trading and swing trading with the required parameters based on your wealth of knowledge, expertise and experiences Shay.  
    """  
  
    
    client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
    )

    response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are the very popular humbled trader also known as Shay. You are also my investment and trading expert advisor and partner.Advise in a tabular format the best parameters given most profitable yet safe day trading and swing trading moves ",
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    #chatHistory=10,
    #max_completion_tokens=800,
    temperature=1.0,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    model=deployment
)

    print(response.choices[0].message.content)
    return response.choices[0].message.content

import requests  
  
import requests  
from openai import AzureOpenAI  
  
  
# Azure OpenAI Configuration  
deployment = "gpt-4.5-preview"  # Replace with your deployment name  
  
# Initialize Azure OpenAI client  
openai = AzureOpenAI(api_key=subscription_key, azure_endpoint=endpoint, api_version=api_version)  
  
import time
import json
import os
from datetime import datetime

# Cache configuration
CACHE_DIR = "cache"
CACHE_FILE = os.path.join(CACHE_DIR, "crypto_data_cache.json")
CACHE_EXPIRY = 15 * 60  # Cache expiry time in seconds (15 minutes)

def fetch_crypto_data_coingecko():
    """
    Fetches cryptocurrency data from the CoinGecko API with caching.
    
    The function will use cached data if available and not expired,
    otherwise it will fetch fresh data from the API.
    
    Returns:
        list: A list of dictionaries containing cryptocurrency data:
            - symbol: Symbol of the cryptocurrency.
            - name: Name of the cryptocurrency.
            - price: Current price of the cryptocurrency.
            - change: 24-hour percentage price change.
            - volume: 24-hour trading volume.
            - market_cap: Market capitalization.
    """
    # Cache configuration for CoinGecko
    COINGECKO_CACHE_FILE = os.path.join(CACHE_DIR, "coingecko_data_cache.json")
    
    # Check if cached data exists and is still valid
    if os.path.exists(COINGECKO_CACHE_FILE):
        try:
            with open(COINGECKO_CACHE_FILE, 'r') as f:
                cache_data = json.load(f)
                
            # Check if cache is still valid
            cache_time = cache_data.get('timestamp', 0)
            current_time = time.time()
            
            if current_time - cache_time < CACHE_EXPIRY:
                print(f"Using cached CoinGecko data from {datetime.fromtimestamp(cache_time).strftime('%Y-%m-%d %H:%M:%S')}")
                return cache_data['data']
            else:
                print("CoinGecko cache expired, fetching fresh data...")
        except Exception as e:
            print(f"Error reading CoinGecko cache: {e}")
    else:
        print("No CoinGecko cache found, fetching fresh data...")
    
    # If we get here, we need to fetch fresh data
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",     # Fetch prices in USD
        "order": "market_cap_desc",  # Sort by market cap
        "per_page": 250,          # Number of results per page (max: 250)
        "page": 1,                # First page
        "sparkline": "false",     # Don't include sparkline data
        "price_change_percentage": "24h"  # Include 24h price change
    }
    
    try:
        response = requests.get(url, params=params)
        
        # Check for rate limiting (CoinGecko has stricter rate limits than CMC)
        if response.status_code == 429:
            print("Rate limit exceeded for CoinGecko API. Waiting and retrying...")
            time.sleep(60)  # Wait for 60 seconds before retrying
            response = requests.get(url, params=params)
            
        if response.status_code == 200:
            data = response.json()
            cryptos = []
            
            for coin in data:
                cryptos.append({
                    "symbol": coin["symbol"].upper(),  # Uppercase for consistency
                    "name": coin["name"],
                    "price": coin["current_price"],
                    "change": coin["price_change_percentage_24h"],
                    "volume": coin["total_volume"],
                    "market_cap": coin["market_cap"],
                })
                
            # Get more data (page 2) to increase coverage
            params["page"] = 2
            response2 = requests.get(url, params=params)
            if response2.status_code == 200:
                data2 = response2.json()
                for coin in data2:
                    cryptos.append({
                        "symbol": coin["symbol"].upper(),
                        "name": coin["name"],
                        "price": coin["current_price"],
                        "change": coin["price_change_percentage_24h"],
                        "volume": coin["total_volume"],
                        "market_cap": coin["market_cap"],
                    })
            
            # Save to cache
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(COINGECKO_CACHE_FILE, 'w') as f:
                json.dump({
                    'timestamp': time.time(),
                    'data': cryptos
                }, f)
                
            print(f"CoinGecko data fetched and cached at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return cryptos
        else:
            print(f"Error fetching data from CoinGecko: {response.status_code} {response.text}")
            return []
    except Exception as e:
        print(f"Exception occurred while fetching CoinGecko data: {e}")
        return []
def fetch_crypto_data_new():  
    """  
    Fetches cryptocurrency data from the CoinMarketCap API with caching.
    
    The function will use cached data if available and not expired,
    otherwise it will fetch fresh data from the API.
  
    Returns:  
        list: A list of dictionaries containing cryptocurrency data:  
            - symbol: Symbol of the cryptocurrency.  
            - name: Name of the cryptocurrency.  
            - price: Current price of the cryptocurrency.  
            - change: 24-hour percentage price change.  
            - volume: 24-hour trading volume.  
            - market_cap: Market capitalization.  
    """
    # Check if cached data exists and is still valid
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                cache_data = json.load(f)
                
            # Check if cache is still valid
            cache_time = cache_data.get('timestamp', 0)
            current_time = time.time()
            
            if current_time - cache_time < CACHE_EXPIRY:
                print(f"Using cached data from {datetime.fromtimestamp(cache_time).strftime('%Y-%m-%d %H:%M:%S')}")
                return cache_data['data']
            else:
                print("Cache expired, fetching fresh data...")
        except Exception as e:
            print(f"Error reading cache: {e}")
    else:
        print("No cache found, fetching fresh data...")
    
    # If we get here, we need to fetch fresh data
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"  
    headers = {  
        "Accepts": "application/json",  
        "X-CMC_PRO_API_KEY": CMC_API_KEY,  
    }  
    params = {  
        "start": 1,  # Start from the top-ranked crypto  
        "limit": 800,  # Fetch the top 800 cryptocurrencies  
        "convert": "USD",  # Convert prices to USD  
    }  
  
    try:  
        response = requests.get(url, headers=headers, params=params)  
        if response.status_code == 200:  
            data = response.json()  
            cryptos = []  
            for crypto in data["data"]:  
                cryptos.append({  
                    "symbol": crypto["symbol"],  
                    "name": crypto["name"],  
                    "price": crypto["quote"]["USD"]["price"],  
                    "change": crypto["quote"]["USD"]["percent_change_24h"],  
                    "volume": crypto["quote"]["USD"]["volume_24h"],  
                    "market_cap": crypto["quote"]["USD"]["market_cap"],  
                })
                
            # Save to cache
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(CACHE_FILE, 'w') as f:
                json.dump({
                    'timestamp': time.time(),
                    'data': cryptos
                }, f)
                
            print(f"Data fetched and cached at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return cryptos  
        else:  
            print(f"Error fetching data from CoinMarketCap: {response.status_code} {response.text}")  
            return []  
    except Exception as e:  
        print(f"Exception occurred while fetching data: {e}")  
        return []
import time
import requests
from ratelimit import limits, sleep_and_retry
from backoff import on_exception, expo

# Define rate limit: 30 calls per 60 seconds
CALLS = 20
RATE_LIMIT = 60

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
@on_exception(expo, requests.exceptions.RequestException, max_tries=10)
def get_crypto_historical_data_coingecko(coin_id, days=30, currency='usd'):
    """
    Fetch historical price data from CoinGecko without plotting a chart.
    
    Parameters:
    - coin_id: CoinGecko coin ID (e.g., 'bitcoin', 'ethereum')
    - days: Number of past days to retrieve data ('1', '7', '14', '30', '90', '180', '365', 'max')
    - currency: Quote currency (default 'usd')
    
    Returns:
    - Dictionary containing historical data with keys:
      - 'dates': List of datetime objects
      - 'prices': List of prices
      - 'volumes': List of trading volumes
      - 'market_caps': List of market capitalizations
    """
    # API endpoint
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
    
    # Request parameters
    params = {
        'vs_currency': currency,
        'days': days,
        'interval': 'daily' if int(days) >= 2 else 'hourly'
    }
    
    # API request
    response = requests.get(url, params=params)
    
    if response.status_code == 429:
        # If we hit the rate limit, sleep for a while and let the decorator retry
        time.sleep(60)
        raise requests.exceptions.RequestException("Rate limit exceeded")
    
    response.raise_for_status()  # This will raise an exception for 4xx and 5xx status codes
    
    data = response.json()
    
    if 'prices' not in data:
        print("No price data returned from API.")
        return None
    
    # Extract timestamps, prices, volumes, and market caps
    timestamps = [price_point[0] for price_point in data['prices']]
    prices = [price_point[1] for price_point in data['prices']]
    
    # Convert timestamps from milliseconds to datetime
    dates = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]
    
    # Extract volumes and market caps if available
    volumes = [volume_point[1] for volume_point in data.get('total_volumes', [])] if 'total_volumes' in data else []
    market_caps = [cap_point[1] for cap_point in data.get('market_caps', [])] if 'market_caps' in data else []
    
    # Calculate some basic technical indicators
    if len(prices) >= 14:
        # Simple Moving Averages
        sma7 = sum(prices[-7:]) / 7
        sma14 = sum(prices[-14:]) / 14
        
        # Price change percentages
        price_change_7d = ((prices[-1] / prices[-7]) - 1) * 100 if prices[-7] > 0 else 0
        price_change_14d = ((prices[-1] / prices[-14]) - 1) * 100 if prices[-14] > 0 else 0
        
        # Volatility (standard deviation of daily returns)
        daily_returns = [(prices[i] / prices[i-1] - 1) for i in range(1, len(prices))]
        volatility = (sum([(r - (sum(daily_returns) / len(daily_returns)))**2 for r in daily_returns]) / len(daily_returns))**0.5 * 100
    else:
        sma7 = sma14 = price_change_7d = price_change_14d = volatility = None
    
    return {
        'dates': dates,
        'prices': prices,
        'volumes': volumes,
        'market_caps': market_caps,
        'technical_indicators': {
            'sma7': sma7,
            'sma14': sma14,
            'price_change_7d': price_change_7d,
            'price_change_14d': price_change_14d,
            'volatility': volatility
        }
    }

def screen_cryptos_for_trading(cryptos_data):  
    """
    Screen cryptocurrencies for trading opportunities using current and historical data.
    
    Parameters:
    - cryptos_data: List of dictionaries containing current cryptocurrency data
    
    Returns:
    - String containing the analysis and recommendations
    """
    # Select top cryptocurrencies for detailed analysis (to avoid API rate limits)
    #top_cryptos = sorted(cryptos_data, key=lambda x: x['volume'], reverse=True)[:20]
    top_cryptos = cryptos_data
    # Prepare the input prompt for screening cryptos
    prompt = """  
    Using your insights and strategies from penny stock trading, focusing on factors like volatility, trading volume, price momentum, liquidity, potential risks, market cap size.
    Filter the provided cryptocurrencies for the best possible/most profitable best day trading and swing trading moves, provide the output in a json file (without the initial ```json and all that jazz) with the following attributes:  
    - Symbol  
    - Name  
    - Price  
    - 24-hour Change (%)  
    - 24-hour Volume  
    - Market Cap  
    - Recommendation (e.g., Day Trade, Swing Trade)  
    - Reason for Recommendation  
    - Trading entry,exit,duration,potential return percentage and other aspects
    - Speculated profit for 100 dollars for given recommendation
    
    Here is the list of cryptocurrencies with current and historical data:  
    """
    
    for crypto in top_cryptos:
        #print(crypto)

        symbol = crypto['symbol'].lower()
        print(crypto['name'])
         
        
        # Try to get historical data (handle potential errors)
        try:
            historical_data = get_crypto_historical_data_coingecko(crypto['name'].lower(), days=30)
            if 1==1:
             print(historical_data)
             continue 
       
            if historical_data:
                tech_indicators = historical_data['technical_indicators']
                
                prompt += f"""  
                --- {crypto['symbol']} ({crypto['name']}) ---
                Current Data:
                - Price: ${crypto['price']:.6f}  
                - 24-hour Change: {crypto['change']}%  
                - 24-hour Volume: ${crypto['volume']}  
                - Market Cap: ${crypto['market_cap']}
                
                Historical Analysis (30 days):
                - 7-Day SMA: ${tech_indicators['sma7']:.6f if tech_indicators['sma7'] else 'N/A'}
                - 14-Day SMA: ${tech_indicators['sma14']:.6f if tech_indicators['sma14'] else 'N/A'}
                - 7-Day Price Change: {tech_indicators['price_change_7d']:.2f}% if tech_indicators['price_change_7d'] else 'N/A'
                - 14-Day Price Change: {tech_indicators['price_change_14d']:.2f}% if tech_indicators['price_change_14d'] else 'N/A'
                - 30-Day Volatility: {tech_indicators['volatility']:.2f}% if tech_indicators['volatility'] else 'N/A'
                
                Price trend: {'Above' if tech_indicators['sma7'] and crypto['price'] > tech_indicators['sma7'] else 'Below'} 7-Day SMA
                Volume trend: {'Increasing' if len(historical_data['volumes']) > 2 and historical_data['volumes'][-1] > historical_data['volumes'][-7] else 'Decreasing'} over the last week
                """
            else:
                prompt += f"""  
                --- {crypto['symbol']} ({crypto['name']}) ---
                - Price: ${crypto['price']:.6f}  
                - 24-hour Change: {crypto['change']}%  
                - 24-hour Volume: ${crypto['volume']}  
                - Market Cap: ${crypto['market_cap']}
                
                Note: Historical data not available for this cryptocurrency.
                """
        except Exception as e:
            print(f"Error getting historical data for {symbol}: {e}")
            prompt += f"""  
            --- {crypto['symbol']} ({crypto['name']}) ---
            - Price: ${crypto['price']:.6f}  
            - 24-hour Change: {crypto['change']}%  
            - 24-hour Volume: ${crypto['volume']}  
            - Market Cap: ${crypto['market_cap']}
            
            Note: Error retrieving historical data for this cryptocurrency.
            """
    with open("screeningprompt.txt" , "w") as f:
        f.write(prompt)
    return 2 
    # Call Azure OpenAI to process the prompt  
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are the very popular humbled trader also known as Shay. You are also my investment and trading expert advisor and partner. Your analysis should incorporate both current market data and historical trends to identify the most promising trading opportunities.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=1.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        model=deployment
    )
    
    result = response.choices[0].message.content
    print(result)
    
    # Save the results to a file
    with open("crypto_screener_with_history.txt", "w") as f:
        f.write(result)
        
    return result    
def screen_cryptos_for_trading_old(cryptos_data):  
    
    # Prepare the input prompt for screening cryptos  
    prompt = """  
    Using your insights and strategies from penny stock trading, focusing on factors like volatility, trading volume, price momentum, liquidity, potential risks, market cap size.  
      Filter the provided cryptocurrencies for the best possible/most profitable best day trading and swing trading moves ,provide the output in a json file (without the initial ```json and all that jazz) with the following attributes:  
    - Symbol  
    - Name  
    - Price  
    - 24-hour Change (%)  
    - 24-hour Volume  
    - Market Cap  
    - Recommendation (e.g., Day Trade, Swing Trade)  
    - Reason for Recommendation  
    - Trading entry,exit,duration,potential return percentage and other aspects
     - Speculated profit for 100 dollars for given recommendation
    

    Here is the list of cryptocurrencies:  
    """  
    for crypto in cryptos_data:  
        prompt += f"""  
        - Symbol: {crypto['symbol']}  
        - Name: {crypto['name']}  
        - Price: ${crypto['price']:.4f}  
        - 24-hour Change: {crypto['change']}%  
        - 24-hour Volume: ${crypto['volume']}  
        - Market Cap: ${crypto['market_cap']}  
        """  
  
    # Call Azure OpenAI to process the prompt  
    client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
    )

    response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are the very popular humbled trader also known as Shay. You are also my investment and trading expert advisor and partner. ",
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    #chatHistory=10,
    #max_completion_tokens=800,
    temperature=1.0,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    model=deployment
)
    import json
    print(response.choices[0].message.content)
    with  open("crypto_screener.txt","w") as f:
        f.write(response.choices[0].message.content)
        
    return response.choices[0].message.content
   
# Function to fetch data from CoinGecko  
def fetch_data_from_coingecko():  
    url = "https://api.coingecko.com/api/v3/coins/markets"  
    params = {  
        "vs_currency": "usd",     # Fetch prices in USD  
        "order": "percent_change_24h_desc",  # Sort by 24h % change  
        "per_page": 250,          # Number of results per page (max: 250)  
        "page": 1,                # First page  
        "price_change_percentage": "24h",  # Fetch 24h price change  
    }  
    response = requests.get(url, params=params)  
  
    if response.status_code == 200:  
        data = response.json()  
        crypto_data = []  
        for coin in data:  
            crypto_data.append({  
                "source": "CoinGecko",  
                "symbol": coin['symbol'].upper(),  
                "name": coin['name'],  
                "price": coin['current_price'],  
                "24h_change_%": coin['price_change_percentage_24h'],  
                "24h_volume": coin['total_volume'],  
                "market_cap": coin['market_cap'],  
            })  
        return pd.DataFrame(crypto_data)  
    else:  
        raise Exception(f"Error fetching data from CoinGecko: {response.status_code}, {response.text}")  
  
  
# Function to fetch data from CoinMarketCap  
def fetch_data_from_coinmarketcap():  
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"  
    headers = {  
        "X-CMC_PRO_API_KEY": "24e7dbc7-b1e3-49c0-8e80-79d787f829f5"  # Replace with your API key  
    }  
    params = {  
        "convert": "USD",  # Fetch prices in USD  
        "limit": 1200,      # Number of results  
    }  
    response = requests.get(url, headers=headers, params=params)  
  
    if response.status_code == 200:  
        data = response.json()['data']  
        crypto_data = []  
        for coin in data:  
            crypto_data.append({  
                "source": "CoinMarketCap",  
                "symbol": coin['symbol'],  
                "name": coin['name'],  
                "price": coin['quote']['USD']['price'],  
                "24h_change_%": coin['quote']['USD']['percent_change_24h'],  
                "24h_volume": coin['quote']['USD']['volume_24h'],  
                "market_cap": coin['quote']['USD']['market_cap'],  
            })  
        return pd.DataFrame(crypto_data)  
    else:  
        raise Exception(f"Error fetching data from CoinMarketCap: {response.status_code}, {response.text}")  
  
  
# Function to fetch data from Binance  
def fetch_data_from_binance():  
    url = "https://api.binance.com/api/v3/ticker/24hr"  
    response = requests.get(url)  
  
    if response.status_code == 200:  
        data = response.json()  
        crypto_data = []  
        for coin in data:  
            crypto_data.append({  
                "source": "Binance",  
                "symbol": coin['symbol'],  
                "name": None,  # Binance API does not provide the full name  
                "price": float(coin['lastPrice']),  
                "24h_change_%": float(coin['priceChangePercent']),  
                "24h_volume": float(coin['quoteVolume']),  
                "market_cap": None,  # Binance API does not provide market cap  
            })  
        return pd.DataFrame(crypto_data)  
    else:  
        raise Exception(f"Error fetching data from Binance: {response.status_code}, {response.text}")  
    

def fetch_crypto_data():  
    try:  
        # Fetch data from all sources  
        print("Fetching data from CoinGecko...")  
        #coingecko_data = fetch_data_from_coingecko()  
  
        print("Fetching data from CoinMarketCap...")  
        coinmarketcap_data = fetch_data_from_coinmarketcap()  
        return coinmarketcap_data
  
        print("Fetching data from Binance...")  
        #binance_data = fetch_data_from_binance()  
  
        # Combine all data into a single DataFrame    coinmarketcap_data
        all_data = pd.concat([ coinmarketcap_data], ignore_index=True)  
  
        # Handle duplicates (if the same crypto appears in multiple sources)  
        # Prioritize sources: CoinMarketCap > CoinGecko > Binance  
        all_data = all_data.sort_values(by="source", ascending=True).drop_duplicates(subset="symbol", keep="first")  
  
        print(all_data)
        return all_data  
  
    except Exception as e:  
        raise Exception(f"Error fetching crypto data: {e}")  


# Main script  
if __name__ == "__main__":  
    print("Fetching crypto data ...")  
    try:  
        # Fetch data  
        #crypto_data = fetch_crypto_data_new()
        crypto_data= fetch_crypto_data_coingecko()
        print(crypto_data)  
          
        # Filter cryptos for high movers  
        print("Screening cryptos for potential movers...")  
        screen_cryptos_for_trading(crypto_data)
        # filtered_cryptos = filter_cryptos(  
        #     crypto_data,  
        #     min_volume=10_000_000,  # Minimum $10M 24h trading volume  
        #     min_change=30,          # Minimum 30% daily price change  
        #     max_change=300,         # Maximum 300% daily price change  
        #     max_market_cap=None     # (Optional) Max market cap filter  
        # )  
          
        # Sort by 24h percentage change  
        # filtered_cryptos = filtered_cryptos.sort_values(by='24h_change_%', ascending=False)  
          
        # print("\nTop Cryptos Based on Criteria:\n")  
        # for _, row in filtered_cryptos.iterrows():  
        #     symbol = row['symbol']  
        #     name = row['name']  
        #     price = row['price']  
        #     change = row['24h_change_%']  
        #     volume = row['24h_volume']  
        #     market_cap = row['market_cap']  
  
        #     print(f"Fetching advice for {symbol}")  
        #     advice = get_openai_advice(symbol, name, price, change, volume, market_cap)  
        #     print(advice)  
        #     print("-" * 40)  # Separator for readability  
  
    except Exception as e:  
        print(f"Error fetching data: {e}")  