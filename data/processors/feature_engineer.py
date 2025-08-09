import pandas as pd
import numpy as np

def create_yield_features(weather_df, soil_df):
    """
    Combines weather and soil data to engineer features for yield prediction.
    """
    # Ensure data is sorted by date
    weather_df = weather_df.sort_values('date')
    soil_df = soil_df.sort_values('date')

    # Merge dataframes on date
    combined_df = pd.merge(weather_df, soil_df, on='date', how='inner')

    # Create interaction terms
    combined_df['temp_x_humidity'] = combined_df['temperature'] * combined_df['humidity']
    combined_df['nitrogen_x_ph'] = combined_df['nitrogen_ppm'] * combined_df['ph']

    # Create rolling averages to capture trends
    combined_df['temp_7day_avg'] = combined_df['temperature'].rolling(window=7).mean()
    combined_df['rain_30day_sum'] = combined_df['rainfall'].rolling(window=30).sum()

    # Fill any NaNs created by rolling windows
    combined_df.fillna(method='bfill', inplace=True)

    return combined_df