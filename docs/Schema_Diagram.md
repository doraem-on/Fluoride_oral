# Schema Diagram
```mermaid
erDiagram
PRODUCTS ||--|{ PRODUCT_INGREDIENTS : contains
INGREDIENTS ||--|{ PRODUCT_INGREDIENTS : used_in
```