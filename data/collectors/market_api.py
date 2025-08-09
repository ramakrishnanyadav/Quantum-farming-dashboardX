import requests
from config import settings

class MarketDataCollector:
    """
    Collects commodity market data from the Alpha Vantage API.
    """
    def __init__(self):
        self.api_key = settings.ALPHAVANTAGE_API_KEY
        self.base_url = "https://www.alphavantage.co/query"

    def get_commodity_price(self, commodity='CORN'):
        """
        Fetches the latest monthly price for a given agricultural commodity.
        Valid commodities: CORN, WHEAT, SOYBEANS, RICE
        """
        if not self.api_key or "your_" in self.api_key:
            print("❌ Alpha Vantage API key not configured in .env file.")
            return None

        params = {
            'function': 'COMMODITY_PRICES_MONTHLY',
            'symbol': commodity,
            'apikey': self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if "data" not in data or not data["data"]:
                print(f"⚠️ No market data returned for {commodity}.")
                return None

            # Get the most recent data point
            latest_data = data['data'][0]
            
            processed_data = {
                'commodity': data.get('name'),
                'date': latest_data.get('date'),
                'price': float(latest_data.get('value')),
                'unit': data.get('unit')
            }
            return processed_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Market API Request Failed: {e}")
            return None