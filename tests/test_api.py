import unittest
from data.collectors.weather_api import WeatherDataCollector
from data.collectors.soil_api import SoilDataCollector

class TestApiCollectors(unittest.TestCase):

    def test_weather_api_returns_data(self):
        """
        Test if the weather API returns a dictionary with expected keys.
        Note: This is a basic integration test and requires a valid API key to pass.
        """
        collector = WeatherDataCollector()
        data = collector.get_live_weather()
        if data: # Only run test if API key is present
            self.assertIsInstance(data, dict)
            self.assertIn('temperature', data)
            self.assertIn('humidity', data)

    def test_soil_api_returns_data(self):
        """
        Test if the public SoilGrids API returns a dictionary with expected keys.
        """
        collector = SoilDataCollector()
        data = collector.get_soil_properties()
        self.assertIsInstance(data, dict)
        self.assertIn('soil_ph', data)
        self.assertIn('organic_carbon_percent', data)

if __name__ == '__main__':
    unittest.main()