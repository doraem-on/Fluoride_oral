
import pandas as pd
import os

def run_qa_pipeline(data_dir):
    """CI pipeline for data validation."""
    print("Running QA Validation...")
    errors = 0
    prod_path = os.path.join(data_dir, 'products.csv')
    if os.path.exists(prod_path):
        df = pd.read_csv(prod_path)
        if df.duplicated('Product_ID').any():
            print("[ERROR] Duplicate Product_ID")
            errors += 1
    if errors == 0:
        print("[SUCCESS] Data QA Passed.")
    return errors == 0
