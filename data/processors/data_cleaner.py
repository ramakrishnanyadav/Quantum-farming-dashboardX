import pandas as pd

def clean_dataframe(df):
    """
    Performs basic data cleaning on a pandas DataFrame.
    - Fills missing numerical values with the mean.
    - Fills missing categorical values with the mode.
    - Removes duplicate rows.
    """
    # Handle numerical columns
    for col in df.select_dtypes(include=['number']).columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mean(), inplace=True)
            
    # Handle categorical columns
    for col in df.select_dtypes(include=['object', 'category']).columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)
            
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    return df