# Data Structure Analysis - queryX Database

## Database Overview
- **Source**: RawData/query.xlsx
- **Database**: queryX.db (SQLite)
- **Created**: January 2025
- **Total Records**: 4,706 manufacturing operations

## Data Hierarchy Understanding

### Key Identifiers
1. **KPL** (Komplet) - Complete product/assembly identifier
2. **RN** (Radni Nalog) - Work order identifier  
3. **WC** (Work Center) - Machine/workstation identifier

### Unique Combinations Analysis
- **Total Records**: 4,706 operations
- **Unique KPL**: 599 products/assemblies
- **Unique RN**: 1,746 work orders
- **Unique KPL+RN**: 4,445 combinations
- **Unique KPL+RN+WC**: 4,706 (all records unique)

### Data Structure Logic
```
KPL (Product)
├── RN (Work Order 1)
│   ├── Operation on WC1 (SAV100)
│   └── Operation on WC2 (G1000)
├── RN (Work Order 2)
│   └── Operation on WC1 (SAV100)
└── RN (Work Order 3)
    └── Operation on WC2 (G1000)
```

## Duplicate Analysis Results

### KPL+RN Duplicates Found: 261 records
**Reason**: Same work order (RN) requires operations on multiple work centers

### Example Duplicates:
```
KPL: 885487, RN: 885620
├── SAV100 (Abkant presa "HACO") - 1 operation
└── G1000 (CNC Glodalica Kekeisen 2500) - 1 operation

KPL: 998834, RN: 998882  
├── SAV100 (Abkant presa "HACO") - 1 operation
└── G1000 (CNC Glodalica Kekeisen 2500) - 1 operation
```

## Work Centers Distribution

### SAV100 - Abkant presa "HACO"
- **Operations**: 3,843 (81.7%)
- **Type**: Press brake operations
- **Primary function**: Sheet metal bending

### G1000 - CNC Glodalica Kekeisen 2500  
- **Operations**: 863 (18.3%)
- **Type**: CNC milling operations
- **Primary function**: Precision machining

## Date Range Analysis

### Delivery Dates (datum_isporuke)
- **Range**: 2024-12-27 to 2025-09-04
- **Span**: ~8.5 months of production planning

### Assembly Dates (datum_sastavljanja)  
- **Range**: 2024-12-24 to 2025-08-11
- **Span**: ~7.5 months of assembly scheduling

## Database Schema

### work_orders Table Structure
```sql
CREATE TABLE work_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kpl INTEGER NOT NULL,                    -- Product identifier
    kplq INTEGER,                           -- Product quantity
    rn INTEGER NOT NULL,                    -- Work order number
    naziv TEXT NOT NULL,                    -- Operation name/description
    norma REAL,                            -- Standard time (hours)
    quantity INTEGER,                       -- Operation quantity
    zq INTEGER,                            -- Quantity completed
    cq INTEGER,                            -- Current quantity
    wc TEXT,                               -- Work center code
    wcname TEXT,                           -- Work center name
    mto TEXT,                              -- Make-to-order info
    datum_isporuke DATE,                   -- Delivery date
    datum_sastavljanja DATE,               -- Assembly date
    norma_j REAL,                          -- Daily norm
    item TEXT,                             -- Item reference
    promjena TEXT,                         -- Change/modification info
    hitno INTEGER,                         -- Urgency level
    suma_h REAL,                           -- Total hours
    zavrsetak_masinske DATE,               -- Machine completion date
    status TEXT DEFAULT 'pending',         -- Operation status
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes Created
- `idx_kpl` - Product lookup
- `idx_rn` - Work order lookup  
- `idx_wc` - Work center filtering
- `idx_datum_isporuke` - Delivery date sorting
- `idx_datum_sastavljanja` - Assembly date sorting
- `idx_status` - Status filtering

## Data Quality Observations

### Positive Aspects
1. **Complete coverage**: All operations have work center assignments
2. **Date consistency**: Delivery and assembly dates are properly formatted
3. **Hierarchical structure**: Clear KPL → RN → WC relationship
4. **Standard times**: Norma values available for scheduling

### Considerations for Web App
1. **Unique identifier**: Use KPL+RN+WC for individual operations
2. **Grouping logic**: Group by KPL for product-level planning
3. **Work center scheduling**: Separate scheduling per work center
4. **Multi-operation orders**: Handle RN spanning multiple work centers

## Implications for MES Web Application

### Scheduling Strategy
- **Product level**: Optimize by KPL delivery dates
- **Work order level**: Schedule RN considering all required work centers
- **Operation level**: Detailed scheduling per work center

### User Interface Design
- **Product view**: Show KPL with all associated work orders
- **Work order view**: Show RN with operations across work centers  
- **Work center view**: Show all operations for specific machine
- **Drag-drop**: Allow reordering at operation level (KPL+RN+WC)

### Optimization Considerations
- **Cross-work center dependencies**: Some RN require sequential operations
- **Work center capacity**: Balance load between SAV100 and G1000
- **Setup times**: Consider changeover between different products
- **Priority handling**: HITNO field indicates urgent orders

---

Key Findings Summary:
Data Structure:

KPL (599 products) → RN (1,746 work orders) → WC operations (4,706 total)
Correct unique identifier: KPL + RN + WC combination
Work Centers:

SAV100 (Press brake): 3,843 operations (81.7%)
G1000 (CNC milling): 863 operations (18.3%)
Date Ranges:

Delivery: Dec 2024 to Sep 2025 (8.5 months)
Assembly: Dec 2024 to Aug 2025 (7.5 months)
"Duplicates" Explained:

261 work orders (RN) span multiple work centers
This is normal - one work order can require operations on different machines
This analysis will be crucial for designing your web app's scheduling logic. The data structure is actually well-organized for manufacturing - you can now optimize at product level (KPL), work order level (RN), or individual operation level (KPL+RN+WC).

Now I understand! The duplicates occur because the same RN (work order) can have operations on different work centers (WC).

Looking at the example:

KPL: 885487, RN: 885620 appears twice:
Once on SAV100 (Abkant presa "HACO")
Once on G1000 (CNC Glodalica Kekeisen 2500)
This means:

KPL = Complete product/assembly
RN = Work order (can span multiple machines)
KPL + RN + WC = Individual operation (should be unique)
So the correct unique identifier should be KPL + RN + WC combination. This makes sense for manufacturing - one work order might require operations on multiple machines.

The data structure is actually correct - you have 4,706 individual manufacturing operations across different work centers for your production planning system.



*Analysis Date: January 2025*
*Database: queryX.db*
*Records Analyzed: 4,706 operations*