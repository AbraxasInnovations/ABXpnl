import requests
from bs4 import BeautifulSoup
import time

# Function to get price from CoinGecko
def get_price_coingecko(coin_id):
    url = f"https://www.coingecko.com/en/coins/{coin_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.find("span", {"data-target": "price.price"})
        if price_tag:
            return float(price_tag.text.strip().replace("$", "").replace(",", ""))
    except Exception as e:
        print(f"Error fetching CoinGecko price: {e}")
    return None

# Function to get price from Dex Screener
def get_price_dexscreener(pair_address):
    url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{pair_address}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if 'pairs' in data and len(data['pairs']) > 0:
            price = data['pairs'][0]['priceUsd']
            if price:
                return float(price)
            else:
                print(f"No price data available for {pair_address}")
        else:
            print(f"No pair data found for {pair_address}")
    except Exception as e:
        print(f"Error fetching DexScreener price: {e}")
    return None

# Function to get price from KuCoin
def get_price_kucoin(symbol):
    url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}-USDT"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if data['code'] == '200000' and 'data' in data and 'price' in data['data']:
            return float(data['data']['price'])
        else:
            print(f"No price data found for {symbol}")
            print(f"API Response: {data}")  # Debug info
    except Exception as e:
        print(f"Error fetching KuCoin price: {e}")
    return None

# Your positions with size and cost basis
positions = {
    "HYPE": {
        "source": "kucoin",
        "id": "HYPE",
        "size": 100,
        "cost_basis": 24
    },
    "SOL": {
        "source": "kucoin",
        "id": "SOL",
        "size": 1,
        "cost_basis": 200
    },
    "USDC": {
        "source": "kucoin",
        "id": "USDC",
        "size": 676,
        "cost_basis": 1
    },
    "TRUMP": {
        "source": "dexscreener",
        "id": "9d9mb8kooFfaD3SctgZtkxQypkshx6ezhbKio89ixyy2",
        "size": 3.79,
        "cost_basis": 41.894
    }
}

def calculate_portfolio():
    portfolio_data = {
        'positions': [],
        'total_value': 0,
        'total_pnl': 0
    }
    
    for coin, details in positions.items():
        # Get current price based on source
        if details["source"] == "kucoin":
            price = get_price_kucoin(details["id"])
        else:  # dexscreener
            price = get_price_dexscreener(details["id"])
        
        if price:
            # Calculate position metrics
            current_value = price * details["size"]
            cost_value = details["cost_basis"] * details["size"]
            pnl = current_value - cost_value
            
            # Update totals
            portfolio_data['total_value'] += current_value
            portfolio_data['total_pnl'] += pnl
            
            # Add position details
            portfolio_data['positions'].append({
                'coin': coin,
                'size': details['size'],
                'price': price,
                'current_value': current_value,
                'pnl': pnl
            })
        else:
            portfolio_data['positions'].append({
                'coin': coin,
                'error': f"Failed to fetch price for {coin}"
            })
        
        # Add delay to avoid rate limiting
        time.sleep(1)
    
    return portfolio_data

if __name__ == "__main__":
    calculate_portfolio() 