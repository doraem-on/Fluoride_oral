
from src.oralatlas.collector import collect_from_raw
from src.oralatlas.normalizer import normalize_data
from src.oralatlas.validator import run_qa_pipeline
from src.oralatlas.feature_engineering import compute_features
from src.oralatlas.exporter import export_formats
import os

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    raw_dir = os.path.join(base, 'raw_data')
    data_dir = base
    export_dir = os.path.join(base, 'exports')
    
    # Pipeline execution
    # collect_from_raw(raw_dir, os.path.join(data_dir, 'raw_consolidated.csv'))
    # normalize_data(os.path.join(data_dir, 'raw_consolidated.csv'), os.path.join(data_dir, 'normalized.csv'))
    
    if run_qa_pipeline(data_dir):
        compute_features(data_dir)
        export_formats(data_dir, export_dir)

if __name__ == '__main__':
    main()
