import requests
from config import settings

class SoilDataCollector:
    """
    Collects soil data from the SoilGrids REST API.
    SoilGrids is a public API and does not require a key.
    """
    def __init__(self):
        self.base_url = "https://rest.isric.org/soilgrids/v2.0/properties/query"

    def get_soil_properties(self, lat=settings.DEFAULT_LATITUDE, lon=settings.DEFAULT_LONGITUDE):
        """
        Fetches key soil properties for a given location.
        """
        properties = ['phh2o', 'soc', 'cec', 'nitrogen'] # pH, Soil Organic Carbon, Cation Exchange, Nitrogen
        
        params = {
            'lon': lon,
            'lat': lat,
            'property': properties,
            'depth': '0-5cm', # Topsoil
            'value': 'mean'
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Process the complex JSON response into a simple dictionary
            props = data.get('properties', {}).get('layers', [])
            
            processed_data = {}
            for layer in props:
                name = layer.get('name')
                depth_info = layer.get('depths', [{}])[0]
                value = depth_info.get('values', {}).get('mean')

                # SoilGrids units are multiplied; we convert them to standard units.
                if name == 'phh2o': # pH x 10
                    processed_data['soil_ph'] = value / 10.0 if value is not None else 6.5
                elif name == 'soc': # Soil Organic Carbon in dg/kg -> %
                    processed_data['organic_carbon_percent'] = value / 100.0 if value is not None else 1.5
                elif name == 'cec': # Cation Exchange Capacity in mmol(c)/kg -> cmol(c)/kg
                    processed_data['cation_exchange_capacity'] = value / 10.0 if value is not None else 12.0
                elif name == 'nitrogen': # Nitrogen in cg/kg -> g/kg
                    processed_data['nitrogen_g_per_kg'] = value / 100.0 if value is not None else 0.15
            
            return processed_data

        except requests.exceptions.RequestException as e:
            print(f"❌ SoilGrids API Request Failed: {e}")
            return None