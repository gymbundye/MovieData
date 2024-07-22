import pandas as pd

def read_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    df.drop_duplicates(inplace=True)
    df['Picked By'] = df['Picked By'].str.strip().str.lower()
    df['Avg Rating'] = pd.to_numeric(df['Avg Rating'], errors='coerce')
    df = df.dropna(subset=['Avg Rating'])
    return df
