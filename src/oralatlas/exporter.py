
import pandas as pd
import sqlite3
import os
import glob

def export_formats(data_dir, export_dir):
    """Exports CSVs to SQLite, Parquet, and JSON."""
    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))
    if not csv_files:
        return

    # SQLite Export
    conn = sqlite3.connect(os.path.join(export_dir, 'oralatlas.db'))
    for f in csv_files:
        table_name = os.path.basename(f).replace('.csv', '')
        try:
            df = pd.read_csv(f)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            df.to_parquet(os.path.join(export_dir, f"{table_name}.parquet"))
            df.to_json(os.path.join(export_dir, f"{table_name}.json"), orient='records')
        except Exception as e:
            pass # Skip empty or invalid CSVs
    conn.close()
    print("Exported to SQLite, Parquet, and JSON.")
