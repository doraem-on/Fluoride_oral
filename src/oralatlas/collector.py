
import json
import os
import pandas as pd

def collect_from_raw(raw_dir, output_file):
    """Ingests raw JSON drops into a consolidated temporary dataframe."""
    data = []
    for root, _, files in os.walk(raw_dir):
        for f in files:
            if f.endswith('.json'):
                with open(os.path.join(root, f), 'r') as jf:
                    data.extend(json.load(jf))
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Collected {len(df)} raw records.")
    return df
