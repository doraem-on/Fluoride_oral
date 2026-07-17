# Global Oral Care Products Intelligence Dataset (GOPID) 2026
**Alternative names:** OralAtlas 2026 ⭐, Open Oral Care Intelligence Dataset (OOCID)

## 1. Abstract
The Global Oral Care Products Intelligence Dataset (GOPID) 2026, colloquially known as **OralAtlas 2026**, is a standardized, research-grade knowledge base of oral care products globally. Unlike conventional commercial datasets, OralAtlas goes beyond simple product lists by providing a meticulously curated, relational ontology connecting products, manufacturers, standardized ingredients, therapeutic properties, certifications, sustainability indicators, formulation chemistry, and consumer-facing claims. This dataset aims to support advanced scientific analysis, market intelligence, public health research, and machine learning applications within the dental consumer product space.

## 2. Motivation
The oral care market is vast and chemically complex, yet publicly available data is fragmented, non-standardized, and heavily skewed by marketing terminology rather than scientific nomenclature. Researchers, health professionals, and machine learning practitioners lack a cohesive resource to analyze global trends in formulations (e.g., fluoride vs. non-fluoride, prevalence of nano-hydroxyapatite), evaluate sustainability claims against packaging reality, or track the network of parent companies and their subsidiary brands. OralAtlas was conceived to bridge this gap, prioritizing data quality, provenance, and structured ontology over sheer volume.

## 3. Scope
The initial dataset seeds a high-quality foundation of exceptionally well-documented products from major global brands (e.g., Colgate, Crest, Sensodyne, Oral-B, Elmex, Curaprox, Parodontax, Marvis). It focuses on:
- **Identification & Markets:** Product SKUs, parent companies, regional availability, and pricing.
- **Formulation Chemistry:** Standardized ingredient tracking using CAS Numbers and PubChem IDs, active compounds, and fluoride ppm.
- **Therapeutic Claims:** Efficacy claims backed by evidence metadata (e.g., Remineralization, Anti-Cavity).
- **Sustainability & Ethics:** Certifications (ADA, EcoCert, Leaping Bunny), packaging materials, and vegan/cruelty-free status.

## 4. Target Audience
This dataset is designed for:
- **Machine Learning Researchers:** For regression, classification, clustering, and recommendation systems.
- **Data Scientists:** For comprehensive market analysis and network graphs.
- **Dentists & Public Health Researchers:** For analyzing active ingredient trends and safety regulations.
- **Biomedical Engineers:** For studying formulation chemistry and material science in packaging.
- **Product Managers & Consumer Market Analysts:** For competitive intelligence and trend forecasting.
- **Environmental Sustainability Researchers:** For auditing plastic reduction and carbon-neutral claims.

## 5. Data Collection Methodology
Data is collected through manual curation and automated extraction from authoritative sources (manufacturer technical sheets, regulatory filings, and recognized global retailers). Every data point is accompanied by provenance metadata, including `Source_URL`, `Collection_Date`, `Verified_By`, and a `Confidence` score, ensuring traceability and reliability for scientific use.

## 6. Cleaning and Normalization Pipeline
To ensure analytical readiness, the data undergoes rigorous normalization:
- **Unit Standardization:** Volumes are converted to `Volume_ml`, weights to `Weight_g`, concentrations to `Fluoride_ppm`, and prices to `Price_USD`.
- **Ingredient Ontology:** Proprietary ingredient names are mapped to their Canonical Name, CAS Number, and PubChem ID.
- **Boolean Features:** Text-based marketing claims are one-hot encoded into specific boolean features (e.g., `Whitening`, `Sensitive`, `Enamel Repair`) to facilitate immediate machine learning application.

## 7. Validation
A custom validation pipeline (`scripts/validate_dataset.py`) continuously audits the dataset for:
- Duplicate products and ingredients.
- Broken foreign keys in junction tables.
- Valid numerical bounds (e.g., Fluoride ppm within regulatory limits).
- Accurate ISO country codes and impossible prices.
- Logical consistency of certifications (e.g., Vegan status vs. Cruelty-Free).

## 8. Limitations
- **Temporal Validity:** Formulation changes by manufacturers may occur without public notice. The `version_history.csv` tracks major audits.
- **Market Coverage:** The dataset initially prioritizes major global brands; regional or hyper-local indie brands may be underrepresented in early versions.

## 9. Ethics
No proprietary or confidential corporate trade secrets were breached during the compilation of this dataset. All data represents publicly accessible information, regulatory filings, and consumer-facing materials, aggregated for scientific and educational use.

## 10. Update Policy
The dataset will be iteratively updated following a strict versioning protocol (Semantic Versioning), with updates published via the `changelog.md`. Subsequent releases (e.g., v1.1, v2.0) will expand the product volume and refine the ingredient ontology.

## 11. License
Creative Commons Attribution 4.0 International (CC BY 4.0).

## 12. Citation
*(Citation details pending publication DOI)*
