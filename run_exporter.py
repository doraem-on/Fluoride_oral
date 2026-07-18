import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from src.oralatlas.exporter import export_formats

base = os.path.dirname(os.path.abspath(__file__))
export_dir = os.path.join(base, 'exports')
print("Running Exporter...")
export_formats(base, export_dir)
print("Exporter finished successfully.")
