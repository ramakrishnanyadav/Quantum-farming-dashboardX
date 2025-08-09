import requests
from config import settings

class WeatherDataCollector:
    """
    Collects weather data from the OpenWeatherMap API.
    """
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_live_weather(self, lat=settings.DEFAULT_LATITUDE, lon=settings.DEFAULT_LONGITUDE):
        """
        Fetches the current weather for a given latitude and longitude.
        """
        if not self.api_key or "your_" in self.api_key:
            print("❌ OpenWeatherMap API key not configured in .env file.")
            return None

        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'  # Get temperature in Celsius
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            
            # Process and return a clean dictionary
            processed_data = {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'].title(),
                'city': data['name']
            }
            return processed_data
        except requests.exceptions.RequestException as e:
            print(f"❌ API Request Failed: {e}")
            return None