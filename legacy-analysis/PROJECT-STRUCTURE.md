# Legacy Analysis - Original VBA System Structure

## Overview
This folder contains the complete analysis of the original Excel VBA-based production planning system, preserved for reference during the transition to the modern web application.

## Directory Structure

```
legacy-analysis/
├── Draft/                          # Working drafts and prototypes
│   ├── Mladen/                     # User-specific drafts
│   ├── excel schema.xlsx           # Database schema design
│   ├── Plan_1.xlsm                # Planning workbook v1
│   └── Plan_2.xlsm                # Planning workbook v2
│
├── excel_code/                     # VBA source code (original system)
│   ├── Azuriraj_crteze.bas        # Update drawings module
│   ├── Azuriraj_plan_novi.bas     # Main scheduling algorithm
│   ├── Azuriraj_plan_stari.bas    # Legacy scheduling module
│   ├── Dole_gore.bas              # Order sequence management
│   ├── Sheet9.cls                  # Worksheet event handlers
│   ├── Status_nova_masina.bas     # New machine status
│   ├── Status_redoslijed.bas      # Order priority management
│   ├── Status_zavsren_sklop.bas   # Completed assembly status
│   ├── ThisWorkbook.cls           # Workbook event handlers
│   └── ZOOM.bas                   # UI utility functions
│
├── HelperScripts/                  # Python utilities for data processing
│   ├── check_duplicates.py        # Database duplicate analysis
│   ├── create_queryX_db.py        # Excel to SQLite converter
│   └── verify_db.py               # Database verification tool
│
├── RawData/                        # Source data and databases
│   ├── query.xlsx                 # Original Excel data export (4,706 operations)
│   └── queryX.db                  # SQLite database for analysis
│
├── Suggestions/                    # Analysis and recommendations
│   ├── data-structure-analysis.md # Database structure analysis
│   ├── optimization-suggestions.md# Performance optimization ideas
│   ├── web-app-architecture.md    # Web application design
│   ├── technology-stack-decision.md# Technology choices
│   └── database-design-enterprise.md# Enterprise database design
│
└── PROJECT-STRUCTURE.md           # This file
```

## Key Components

### Current System (VBA)
- **Main Algorithm**: `Azuriraj_plan_novi.bas` - Complex shift-based scheduling
- **Data Source**: Excel sheets with work orders and machine calendars
- **Features**: 3-shift scheduling, break management, machine assignments

### Data Layer
- **Source**: `query.xlsx` (4,706 manufacturing operations)
- **Database**: `queryX.db` (SQLite with optimized schema)
- **Structure**: KPL (products) → RN (work orders) → WC (work center operations)

### Future System (Web App)
- **Target**: Node.js + React + PostgreSQL
- **Features**: Date-based optimization, drag-drop scheduling, real-time updates
- **Deployment**: Ubuntu server with Nginx

## Work Centers
- **SAV100**: Abkant presa "HACO" (3,843 operations, 81.7%)
- **G1000**: CNC Glodalica Kekeisen 2500 (863 operations, 18.3%)

## Data Statistics
- **Total Operations**: 4,706
- **Unique Products (KPL)**: 599
- **Unique Work Orders (RN)**: 1,746
- **Date Range**: December 2024 - September 2025
- **Unique Identifier**: KPL + RN + WC combination

## Development Status
- ✅ VBA system analysis complete
- ✅ Data extraction and database creation
- ✅ Architecture planning and optimization analysis
- 🔄 Web application development (planned)
- ⏳ Migration and deployment (future)

## Next Steps
1. Set up Node.js development environment
2. Create PostgreSQL schema based on SQLite analysis
3. Implement basic CRUD operations
4. Port scheduling algorithms from VBA
5. Build drag-drop interface
6. Deploy to Ubuntu server

---
*Last Updated: January 2025*
*Project Status: Analysis & Planning Phase*