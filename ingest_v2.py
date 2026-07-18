import pandas as pd
import numpy as np
import os
import uuid

print("Starting v2.0 ingestion process...")

# 1. Load existing tables
products_df = pd.read_csv('products.csv')
brands_df = pd.read_csv('brands.csv')
categories_df = pd.read_csv('categories.csv')
product_claims_df = pd.read_csv('product_claims.csv')
product_markets_df = pd.read_csv('product_markets.csv')
ingredients_df = pd.read_csv('ingredients.csv')
product_ingredients_df = pd.read_csv('product_ingredients.csv')
countries_df = pd.read_csv('countries.csv')
claims_df = pd.read_csv('claims.csv')

# Load new raw data
mw_df = pd.read_csv('raw_data/verified/oralatlas_mouthwash.csv')
fl_df = pd.read_csv('raw_data/verified/oralatlas_floss.csv')
tb_df = pd.read_csv('raw_data/verified/oralatlas_electric_toothbrush.csv')

# 2. Add New Categories
new_categories = pd.DataFrame({
    'Category_ID': ['CAT_2', 'CAT_3', 'CAT_4'],
    'Category_Name': ['Mouthwash', 'Dental Floss', 'Electric Toothbrush'],
    'Subcategory_Name': ['General', 'General', 'Hardware']
})
categories_df = pd.concat([categories_df, new_categories]).drop_duplicates(subset=['Category_ID'])
categories_df.to_csv('categories.csv', index=False)

# 3. Helpers
existing_brands = brands_df.set_index('Brand_Name')['Brand_ID'].to_dict()
existing_claims = claims_df.set_index('Claim_Name')['Claim_ID'].to_dict()
existing_countries = countries_df.set_index('Country_Name')['Country_ID'].to_dict()
existing_ingredients = ingredients_df.set_index('Canonical_Name')['Ingredient_ID'].to_dict()

brand_counter = len(brands_df) + 1
claim_counter = len(claims_df) + 1
country_counter = len(countries_df) + 1
ingredient_counter = len(ingredients_df) + 1

new_brands = []
new_claims = []
new_countries = []
new_products = []
new_product_claims = []
new_product_markets = []
new_product_ingredients = []
specifications = []

def get_or_create_brand(name, parent=""):
    global brand_counter
    if pd.isna(name): return None
    if name not in existing_brands:
        b_id = f'B_{uuid.uuid4().hex[:8]}'
        existing_brands[name] = b_id
        new_brands.append([b_id, name, parent, 'Global'])
    return existing_brands[name]

def get_or_create_country(name):
    global country_counter
    if pd.isna(name): name = 'Global'
    if name not in existing_countries:
        c_id = f'CTRY_{country_counter}'
        existing_countries[name] = c_id
        new_countries.append([c_id, name[:3].upper(), name, name])
        country_counter += 1
    return existing_countries[name]

def get_or_create_claim(name):
    global claim_counter
    if pd.isna(name): return None
    name = str(name).strip()
    if name not in existing_claims:
        c_id = f'C_{name.replace(" ", "_")}'
        existing_claims[name] = c_id
        new_claims.append([c_id, name, 'Marketing', ''])
        claim_counter += 1
    return existing_claims[name]

def get_or_create_ingredient(name, is_active="Yes"):
    global ingredient_counter
    if pd.isna(name): return None
    name = str(name).strip()
    if name not in existing_ingredients:
        i_id = f'ING_{ingredient_counter}'
        existing_ingredients[name] = i_id
        new_ingredients.append([i_id, name, is_active])
        ingredient_counter += 1
    return existing_ingredients[name]

new_ingredients = []

# --- Process Mouthwash ---
for _, row in mw_df.iterrows():
    p_id = row['Product ID']
    b_id = get_or_create_brand(row['Brand'], row.get('Parent Company', ''))
    c_id = get_or_create_country(row.get('Country/Region', 'Global'))
    
    new_products.append([p_id, row['Product Name'], b_id, 'CAT_2', 'Kids' if str(row.get('Kids'))=='Yes' else 'Adult', 100])
    new_product_markets.append([p_id, c_id, '', '', 'Yes', 'Yes', '', '', ''])
    
    # Claims
    for claim_col in ['Whitening', 'Sensitivity Relief', 'Gum Care', 'Fresh Breath', 'Antibacterial/Antiplaque']:
        if str(row.get(claim_col)) == 'Yes':
            claim_id = get_or_create_claim(claim_col)
            new_product_claims.append([p_id, claim_id])
            
    # Ingredients
    if str(row.get('Alcohol')) == 'Yes':
        new_product_ingredients.append([p_id, get_or_create_ingredient('Alcohol', 'No')])
    if str(row.get('Fluoride')) == 'Yes':
        new_product_ingredients.append([p_id, get_or_create_ingredient('Sodium Fluoride', 'Yes')])

# --- Process Floss ---
for _, row in fl_df.iterrows():
    p_id = row['Product ID']
    b_id = get_or_create_brand(row['Brand'], row.get('Parent Company', ''))
    c_id = get_or_create_country(row.get('Country/Region', 'Global'))
    
    new_products.append([p_id, row['Product Name'], b_id, 'CAT_3', 'Adult', 100])
    new_product_markets.append([p_id, c_id, '', '', 'Yes', 'Yes', '', '', ''])
    
    # Specifications
    if pd.notna(row.get('Floss Type')):
        specifications.append([p_id, 'Floss Type', row['Floss Type']])
    if pd.notna(row.get('Waxed')):
        specifications.append([p_id, 'Waxed', row['Waxed']])
    if pd.notna(row.get('Flavor')):
        specifications.append([p_id, 'Flavor', row['Flavor']])

# --- Process Electric Toothbrush ---
for _, row in tb_df.iterrows():
    p_id = row['Product ID']
    b_id = get_or_create_brand(row['Brand'], row.get('Parent Company', ''))
    c_id = get_or_create_country(row.get('Country/Region', 'Global'))
    
    new_products.append([p_id, row['Product Name'], b_id, 'CAT_4', 'Adult', 100])
    new_product_markets.append([p_id, c_id, '', '', 'Yes', 'Yes', '', '', ''])
    
    # Specifications
    if pd.notna(row.get('Brush Type')):
        specifications.append([p_id, 'Brush Type', row['Brush Type']])
    if pd.notna(row.get('Pressure Sensor')):
        specifications.append([p_id, 'Pressure Sensor', row['Pressure Sensor']])
    if pd.notna(row.get('App Connectivity')):
        specifications.append([p_id, 'App Connectivity', row['App Connectivity']])

# 4. Append to CSVs
if new_brands:
    pd.DataFrame(new_brands, columns=['Brand_ID', 'Brand_Name', 'Manufacturer_ID', 'Region']).to_csv('brands.csv', mode='a', header=False, index=False)
if new_countries:
    pd.DataFrame(new_countries, columns=['Country_ID', 'Country_Code', 'Country_Name', 'Region']).to_csv('countries.csv', mode='a', header=False, index=False)
if new_claims:
    pd.DataFrame(new_claims, columns=['Claim_ID', 'Claim_Name', 'Category', 'Description']).to_csv('claims.csv', mode='a', header=False, index=False)
if new_ingredients:
    pd.DataFrame(new_ingredients, columns=['Ingredient_ID', 'Canonical_Name', 'Active']).to_csv('ingredients.csv', mode='a', header=False, index=False)
if new_products:
    pd.DataFrame(new_products, columns=['Product_ID', 'Product_Name', 'Brand_ID', 'Category_ID', 'Target_Audience', 'Data_Quality']).to_csv('products.csv', mode='a', header=False, index=False)
if new_product_claims:
    pd.DataFrame(new_product_claims, columns=['Product_ID', 'Claim_ID']).to_csv('product_claims.csv', mode='a', header=False, index=False)
if new_product_markets:
    pd.DataFrame(new_product_markets, columns=['Product_ID', 'Country_ID', 'Launch_Date', 'Discontinued', 'Online_Available', 'Retail_Available', 'Price_USD', 'Volume_ml', 'Weight_g']).to_csv('product_markets.csv', mode='a', header=False, index=False)
if new_product_ingredients:
    pd.DataFrame(new_product_ingredients, columns=['Product_ID', 'Ingredient_ID']).to_csv('product_ingredients.csv', mode='a', header=False, index=False)

# 5. Create product_specifications.csv
spec_df = pd.DataFrame(specifications, columns=['Product_ID', 'Spec_Name', 'Spec_Value'])
# Check if file exists to append or create
if os.path.exists('product_specifications.csv'):
    spec_df.to_csv('product_specifications.csv', mode='a', header=False, index=False)
else:
    spec_df.to_csv('product_specifications.csv', index=False)

print("v2.0 Ingestion Complete! Data successfully appended to core tables and product_specifications.csv created.")
