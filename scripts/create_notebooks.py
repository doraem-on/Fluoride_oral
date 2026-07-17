import json, os

notebooks = [
    "01_Data_Collection_and_Cleaning.ipynb",
    "02_Global_Oral_Care_Landscape.ipynb",
    "03_Ingredient_Network_Analysis.ipynb",
    "04_Fluoride_vs_NonFluoride.ipynb",
    "05_Sustainability_and_Certifications.ipynb",
    "06_Product_Recommendation_System.ipynb",
    "07_Baseline_Machine_Learning.ipynb",
    "08_Interactive_Dashboard.ipynb"
]

for nb in notebooks:
    title = nb.replace("_", " ").replace(".ipynb", "")
    content = {
        "cells": [{
            "cell_type": "markdown",
            "metadata": {},
            "source": [f"# {title}"]
        }],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5
    }
    with open(f"/Users/lalit/kaggle_datasets/Fluoride_oral/notebooks/{nb}", "w") as f:
        json.dump(content, f, indent=2)

print("Notebooks created successfully.")
