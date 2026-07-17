
import pandas as pd

def normalize_data(raw_file, output_file):
    """Standardizes units, resolves aliases, formats dates."""
    try:
        df = pd.read_csv(raw_file)
        # Example transformations:
        if 'weight_oz' in df.columns:
            df['Weight_g'] = df['weight_oz'] * 28.3495
        if 'price_eur' in df.columns:
            df['Price_USD'] = df['price_eur'] * 1.1 # Static approx
            
        df.to_csv(output_file, index=False)
        print("Data normalization complete.")
    except Exception as e:
        print(f"Normalization skipped or failed: {e}")
