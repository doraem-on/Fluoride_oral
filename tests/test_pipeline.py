import os
import sys
import pandas as pd
import sqlite3

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.oralatlas.normalizer import normalize_data
from src.oralatlas.validator import run_qa_pipeline

def test_normalization(tmp_path):
    raw_file = tmp_path / "raw.csv"
    out_file = tmp_path / "out.csv"
    df = pd.DataFrame([{"weight_oz": 1.0, "price_eur": 1.0}])
    df.to_csv(raw_file, index=False)
    
    normalize_data(str(raw_file), str(out_file))
    result = pd.read_csv(out_file)
    assert abs(result['Weight_g'].iloc[0] - 28.3495) < 0.001
    assert abs(result['Price_USD'].iloc[0] - 1.1) < 0.001

def test_validator_duplicates(tmp_path):
    prod_file = tmp_path / "products.csv"
    df = pd.DataFrame([{"Product_ID": "1"}, {"Product_ID": "1"}])
    df.to_csv(prod_file, index=False)
    # Should fail due to duplicates
    assert not run_qa_pipeline(str(tmp_path))
