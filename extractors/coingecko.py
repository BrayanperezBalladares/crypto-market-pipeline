import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("COINGECKO_BASE_URL", "https://api.coingecko.com/api/v3")
TOP_N_COINS = int(os.getenv("COINGECKO_TOP_N_COINS", 50))


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def fetch_top_coins(vs_currency: str = "usd", per_page: int = TOP_N_COINS) -> list[dict]:
    """
    Fetch top coins by market cap from CoinGecko API.
    Retries up to 3 times with exponential backoff if the request fails.
    """
    url = f"{BASE_URL}/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h,7d,30d"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def extract_coins() -> list[dict]:
    """
    Main extraction function. Fetches top coins and returns raw data.
    """
    print("Extracting top coins from CoinGecko...")
    coins = fetch_top_coins()
    print(f"Extracted {len(coins)} coins successfully.")
    return coins


if __name__ == "__main__":
    data = extract_coins()
    for coin in data[:3]:
        print(f"{coin['symbol'].upper()} | ${coin['current_price']:,.2f} | Cap: ${coin['market_cap']:,.0f}")