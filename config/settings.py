"""
Configuration settings for Quantum Smart Farming Dashboard, loaded from .env
"""
import os
from dotenv import load_dotenv

# Load variables from .env file in the root directory
load_dotenv()

# --- API Configuration ---
# You can get free keys for these services to enable live data.
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

# --- Application Settings ---
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
CACHE_DURATION = int(os.getenv('CACHE_DURATION', '300'))

# --- Quantum Configuration ---
QUANTUM_BACKEND = os.getenv('QUANTUM_BACKEND', 'aer_simulator')
DEFAULT_SHOTS = int(os.getenv('DEFAULT_SHOTS', '1024'))

# --- Geographic Data ---
# Default location if live data fails
DEFAULT_LATITUDE = 19.0760
DEFAULT_LONGITUDE = 72.8777

# Farm Locations with Coordinates for Live Data Feature
# THIS IS THE DICTIONARY THAT WAS MISSING
FARM_LOCATIONS = {
    "Maharashtra, India": {'lat': 19.0760, 'lon': 72.8777, 'city': 'Mumbai'},
    "California, USA": {'lat': 36.7783, 'lon': -119.4179, 'city': 'Fresno'},
    "Bavaria, Germany": {'lat': 48.7904, 'lon': 11.4979, 'city': 'Ingolstadt'},
    "São Paulo, Brazil": {'lat': -23.5505, 'lon': -46.6333, 'city': 'São Paulo'},
}