import os
import shutil
import json
import csv

BASE_DIR = '/Users/lalit/kaggle_datasets/Fluoride_oral'

# 1. Directory Reorganization
os.makedirs(os.path.join(BASE_DIR, 'raw_data', 'verified'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'raw_data', 'demo'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'schemas'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'tests'), exist_ok=True)

# Move existing raw files to demo
raw_dir = os.path.join(BASE_DIR, 'raw_data')
for f in os.listdir(raw_dir):
    if f.endswith('.json'):
        shutil.move(os.path.join(raw_dir, f), os.path.join(raw_dir, 'demo', f))

# 2. Ingestion Schema
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "OralAtlas Ingestion Schema",
    "type": "object",
    "required": ["source_url", "collection_date", "brand", "product_name"],
    "properties": {
        "source_url": {"type": "string", "format": "uri"},
        "collection_date": {"type": "string", "format": "date"},
        "verification_status": {"type": "string", "enum": ["Verified", "Pending", "Demo"]},
        "confidence": {"type": "string", "enum": ["High", "Medium", "Low"]},
        "brand": {"type": "string"},
        "product_name": {"type": "string"},
        "ingredients": {
            "type": "array",
            "items": {"type": "string"}
        },
        "claims": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}
with open(os.path.join(BASE_DIR, 'schemas', 'ingestion_schema.json'), 'w') as f:
    json.dump(schema, f, indent=4)

# 3. Source Registry
with open(os.path.join(BASE_DIR, 'source_registry.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Source_Name', 'Official_URL', 'Region', 'Data_Available', 'Scraping_Method', 'Last_Collection', 'Reliability_Score'])
    writer.writerow(['Colgate', 'https://www.colgate.com', 'Global', 'Ingredients, Claims', 'API/Scraper', '', 'High'])
    writer.writerow(['Sensodyne', 'https://www.sensodyne.com', 'Global', 'Ingredients, Claims', 'API/Scraper', '', 'High'])
    writer.writerow(['Crest', 'https://www.crest.com', 'North America', 'Ingredients, Claims', 'API/Scraper', '', 'High'])
    writer.writerow(["Tom's of Maine", 'https://www.tomsofmaine.com', 'North America', 'Ingredients, Sustainability', 'API/Scraper', '', 'High'])

# 4. Tests
test_content = """import os
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
"""
with open(os.path.join(BASE_DIR, 'tests', 'test_pipeline.py'), 'w') as f:
    f.write(test_content)

# 5. Update pipeline to use verified/
pipeline_path = os.path.join(BASE_DIR, 'pipeline.py')
with open(pipeline_path, 'r') as f:
    content = f.read()
content = content.replace("raw_dir = os.path.join(base, 'raw_data')", "raw_dir = os.path.join(base, 'raw_data', 'verified')")
with open(pipeline_path, 'w') as f:
    f.write(content)

# 6. Update Schema Diagram
schema_diagram = """# Schema Diagram

```mermaid
erDiagram
    MANUFACTURERS ||--|{ BRANDS : owns
    BRANDS ||--|{ PRODUCTS : manufactures
    PRODUCTS ||--|{ PRODUCT_INGREDIENTS : contains
    INGREDIENTS ||--|{ PRODUCT_INGREDIENTS : used_in
    PRODUCTS ||--|{ PRODUCT_CLAIMS : asserts
    CLAIMS ||--|{ PRODUCT_CLAIMS : categorizes
    PRODUCTS ||--|{ PRODUCT_MARKETS : sold_in
    COUNTRIES ||--|{ PRODUCT_MARKETS : location
```
"""
with open(os.path.join(BASE_DIR, 'docs', 'Schema_Diagram.md'), 'w') as f:
    f.write(schema_diagram)

print("Phase 3 setup completed.")
