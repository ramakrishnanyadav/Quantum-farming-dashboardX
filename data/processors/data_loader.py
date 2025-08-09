import pandas as pd
import os

DATA_DIR = 'data/sample_data'

def load_all_data():
    """Loads all sample CSVs into a dictionary of pandas DataFrames."""
    all_data = {}
    try:
        files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
        for file in files:
            key = file.replace('_data.csv', '')
            all_data[key] = pd.read_csv(os.path.join(DATA_DIR, file), parse_dates=['date'])
        print("✅ Sample data loaded successfully.")
        return all_data
    except FileNotFoundError:
        print(f"❌ Error: Data directory not found at '{DATA_DIR}'. Please run setup.py.")
        return None