
import pandas as pd
import os

def compute_features(data_dir):
    """Generates product_derived_features.csv."""
    pi_path = os.path.join(data_dir, 'product_ingredients.csv')
    if not os.path.exists(pi_path):
        return
        
    pi = pd.read_csv(pi_path)
    # Feature 1: Ingredient Count
    counts = pi.groupby('Product_ID').size().reset_index(name='Ingredient_Count')
    
    # Feature 2: Active Ingredient Count (Mock logic)
    counts['Active_Ingredient_Count'] = (counts['Ingredient_Count'] * 0.2).astype(int)
    
    # Feature 3: Sustainability Score (Mock logic)
    counts['Sustainability_Score'] = 75 
    
    counts.to_csv(os.path.join(data_dir, 'product_derived_features.csv'), index=False)
    print("Computed derived features.")
