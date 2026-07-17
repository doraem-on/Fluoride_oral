import os
import pandas as pd
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_data(filename):
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath):
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return None
    return None

def run_validations():
    print("--- Starting OralAtlas 2026 Validation Pipeline ---")
    
    products = load_data('products.csv')
    ingredients = load_data('ingredients.csv')
    brands = load_data('brands.csv')
    product_ingredients = load_data('product_ingredients.csv')
    product_markets = load_data('product_markets.csv')
    
    errors = 0

    if products is not None and not products.empty:
        # Check duplicates
        if products.duplicated('Product_ID').any():
            print("[ERROR] Duplicate Product_ID found in products.csv")
            errors += 1
            
        # Check missing brand references if brands exist
        if brands is not None and not brands.empty:
            missing_brands = set(products['Brand_ID'].dropna()) - set(brands['Brand_ID'])
            if missing_brands:
                print(f"[ERROR] Broken Foreign Key: Brand_IDs {missing_brands} in products.csv not found in brands.csv")
                errors += 1

    if ingredients is not None and not ingredients.empty:
        if ingredients.duplicated('Ingredient_ID').any():
            print("[ERROR] Duplicate Ingredient_ID found in ingredients.csv")
            errors += 1

    if product_ingredients is not None and not product_ingredients.empty:
        # Validate Fluoride PPM ranges
        if 'Fluoride_ppm' in product_ingredients.columns:
            invalid_fluoride = product_ingredients[
                (product_ingredients['Fluoride_ppm'] < 0) | 
                (product_ingredients['Fluoride_ppm'] > 5000)
            ]
            if not invalid_fluoride.empty:
                print("[ERROR] Invalid Fluoride_ppm values detected (must be between 0 and 5000).")
                errors += 1

        # Check FK integrity
        if products is not None and not products.empty:
            missing_products = set(product_ingredients['Product_ID'].dropna()) - set(products['Product_ID'])
            if missing_products:
                print(f"[ERROR] Broken Foreign Key: Product_IDs {missing_products} in product_ingredients.csv not found in products.csv")
                errors += 1
                
        if ingredients is not None and not ingredients.empty:
            missing_ings = set(product_ingredients['Ingredient_ID'].dropna()) - set(ingredients['Ingredient_ID'])
            if missing_ings:
                print(f"[ERROR] Broken Foreign Key: Ingredient_IDs {missing_ings} in product_ingredients.csv not found in ingredients.csv")
                errors += 1

    if product_markets is not None and not product_markets.empty:
        if 'Price_USD' in product_markets.columns:
            invalid_prices = product_markets[product_markets['Price_USD'] < 0]
            if not invalid_prices.empty:
                print("[ERROR] Impossible prices (Price_USD < 0) found in product_markets.csv")
                errors += 1

    if errors == 0:
        print("[SUCCESS] All validations passed. Dataset integrity is maintained.")
        sys.exit(0)
    else:
        print(f"[FAILED] {errors} validation errors found.")
        sys.exit(1)

if __name__ == "__main__":
    run_validations()
