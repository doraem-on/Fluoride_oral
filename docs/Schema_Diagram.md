# Schema Diagram

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
