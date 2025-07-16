# Enterprise MES Database Design

## Overview
This database design supports a full-scale Manufacturing Execution System with multi-level planning (plant floor, mid-level, high-level), complete audit trails, and hierarchical product structures.

## Core Entity Relationships

```
Organizations
├── Plants
│   ├── Work Centers
│   │   └── Operations (scheduling units)
│   └── Product Hierarchies
│       ├── Products (KPL level)
│       ├── Sub-assemblies
│       └── Components
└── Users & Audit Trail
```

## Database Schema

### 1. Organizational Structure

```sql
-- Organizations (multi-plant support)
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Plants within organizations
CREATE TABLE plants (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id),
    code VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    location VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(organization_id, code)
);

-- Work center categories (flexible types)
CREATE TABLE work_center_categories (
    id SERIAL PRIMARY KEY,
    category_code VARCHAR(20) UNIQUE NOT NULL,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    default_setup_time_minutes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Work centers within plants
CREATE TABLE work_centers (
    id SERIAL PRIMARY KEY,
    plant_id INTEGER REFERENCES plants(id),
    code VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES work_center_categories(id),
    capacity_hours_per_day DECIMAL(4,2) DEFAULT 8.0,
    setup_time_minutes INTEGER DEFAULT 0,
    cost_per_hour DECIMAL(10,2),
    additional_data JSONB,           -- Flexible attributes
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(plant_id, code)
);

-- Work center substitutions (alternative work centers)
CREATE TABLE work_center_substitutions (
    id SERIAL PRIMARY KEY,
    primary_work_center_id INTEGER REFERENCES work_centers(id),
    substitute_work_center_id INTEGER REFERENCES work_centers(id),
    substitution_factor DECIMAL(4,2) DEFAULT 1.0, -- Time multiplier
    cost_factor DECIMAL(4,2) DEFAULT 1.0,         -- Cost multiplier
    priority_order INTEGER DEFAULT 0,              -- Preference order
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(primary_work_center_id, substitute_work_center_id)
);
```

### 2. Flexible Product Hierarchy (Multi-level BOM)

```sql
-- Product types (flexible categories)
CREATE TABLE product_types (
    id SERIAL PRIMARY KEY,
    type_code VARCHAR(20) UNIQUE NOT NULL, -- 'PRODUCT', 'ASSEMBLY', 'COMPONENT'
    type_name VARCHAR(100) NOT NULL,
    description TEXT,
    can_have_children BOOLEAN DEFAULT true,
    sort_order INTEGER DEFAULT 0
);

-- Products with flexible hierarchical structure
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    kpl VARCHAR(50) UNIQUE NOT NULL,  -- Your current KPL identifier
    product_type_id INTEGER REFERENCES product_types(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    specifications JSONB,             -- Flexible product specs
    cost_data JSONB,                 -- Cost information
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Bill of Materials (BOM) - flexible parent-child relationships
CREATE TABLE bom_structure (
    id SERIAL PRIMARY KEY,
    parent_product_id INTEGER REFERENCES products(id),
    child_product_id INTEGER REFERENCES products(id),
    quantity_required DECIMAL(10,4) DEFAULT 1.0,
    bom_level INTEGER NOT NULL,      -- 0=top, 1=first level, etc.
    sequence_order INTEGER DEFAULT 0,
    effective_date DATE DEFAULT CURRENT_DATE,
    expiry_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(parent_product_id, child_product_id, effective_date)
);

-- BOM hierarchy path (for quick lookups)
CREATE TABLE bom_hierarchy_paths (
    id SERIAL PRIMARY KEY,
    ancestor_product_id INTEGER REFERENCES products(id),
    descendant_product_id INTEGER REFERENCES products(id),
    path_length INTEGER NOT NULL,    -- Distance in hierarchy
    path_data JSONB,                -- Full path information
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(ancestor_product_id, descendant_product_id)
);

-- Product routing (which work centers are needed)
CREATE TABLE product_routings (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    work_center_id INTEGER REFERENCES work_centers(id),
    sequence_order INTEGER NOT NULL,
    standard_time_hours DECIMAL(8,2),
    setup_time_minutes INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(product_id, work_center_id, sequence_order)
);
```

### 3. Work Orders & Operations

```sql
-- Work orders (your RN level)
CREATE TABLE work_orders (
    id SERIAL PRIMARY KEY,
    rn VARCHAR(50) UNIQUE NOT NULL,  -- Your current RN identifier
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    priority_level INTEGER DEFAULT 0, -- Your HITNO field
    datum_isporuke DATE,              -- Delivery date
    datum_sastavljanja DATE,          -- Assembly date
    datum_treci DATE,                 -- Third date field
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Individual operations (your current KPL+RN+WC level)
CREATE TABLE operations (
    id SERIAL PRIMARY KEY,
    work_order_id INTEGER REFERENCES work_orders(id),
    work_center_id INTEGER REFERENCES work_centers(id),
    operation_sequence INTEGER NOT NULL,
    naziv VARCHAR(200) NOT NULL,      -- Operation name
    norma DECIMAL(8,2),              -- Standard time hours
    quantity INTEGER,
    quantity_completed INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    dependencies JSONB,               -- For complex dependencies
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(work_order_id, work_center_id) -- One op per WO per WC
);
```

### 4. Scheduling System

```sql
-- Scheduling scenarios (multiple planning levels)
CREATE TABLE scheduling_scenarios (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    scenario_type VARCHAR(50), -- 'PLANT_FLOOR', 'MID_LEVEL', 'HIGH_LEVEL'
    plant_id INTEGER REFERENCES plants(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Schedule entries (actual scheduling data)
CREATE TABLE schedule_entries (
    id SERIAL PRIMARY KEY,
    scenario_id INTEGER REFERENCES scheduling_scenarios(id),
    operation_id INTEGER REFERENCES operations(id),
    work_center_id INTEGER REFERENCES work_centers(id),
    sequence_order INTEGER NOT NULL,
    planned_start TIMESTAMP,
    planned_end TIMESTAMP,
    actual_start TIMESTAMP,
    actual_end TIMESTAMP,
    status VARCHAR(20) DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(scenario_id, work_center_id, sequence_order)
);

-- Schedule history (track all changes)
CREATE TABLE schedule_history (
    id SERIAL PRIMARY KEY,
    schedule_entry_id INTEGER REFERENCES schedule_entries(id),
    old_sequence_order INTEGER,
    new_sequence_order INTEGER,
    old_planned_start TIMESTAMP,
    new_planned_start TIMESTAMP,
    change_reason VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    created_by INTEGER REFERENCES users(id)
);
```

### 5. Real-time Operation Tracking

```sql
-- Operation time stamps (your start/stop registration system)
CREATE TABLE operation_timestamps (
    id SERIAL PRIMARY KEY,
    operation_id INTEGER REFERENCES operations(id),
    work_center_id INTEGER REFERENCES work_centers(id),
    timestamp_type VARCHAR(20) NOT NULL, -- 'START', 'STOP', 'PAUSE', 'RESUME'
    timestamp_value TIMESTAMP NOT NULL,
    operator_id INTEGER REFERENCES users(id),
    workstation_identifier VARCHAR(100), -- PC name, terminal ID, etc.
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Operation status tracking
CREATE TABLE operation_status_log (
    id SERIAL PRIMARY KEY,
    operation_id INTEGER REFERENCES operations(id),
    old_status VARCHAR(20),
    new_status VARCHAR(20),
    status_reason VARCHAR(500),
    changed_at TIMESTAMP DEFAULT NOW(),
    changed_by INTEGER REFERENCES users(id),
    workstation_identifier VARCHAR(100)
);
```

### 6. User Management & Audit System

```sql
-- Users and roles
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(200),
    full_name VARCHAR(200),
    role VARCHAR(50), -- 'PLANNER', 'SUPERVISOR', 'OPERATOR', 'ADMIN'
    plant_id INTEGER REFERENCES plants(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Comprehensive audit log
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
    old_values JSONB,
    new_values JSONB,
    user_id INTEGER REFERENCES users(id),
    session_id VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    workstation_identifier VARCHAR(100),
    change_reason VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Session tracking
CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    workstation_identifier VARCHAR(100),
    login_at TIMESTAMP DEFAULT NOW(),
    logout_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);
```

### 7. Configuration & Metadata

```sql
-- System configuration
CREATE TABLE system_config (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value JSONB,
    description TEXT,
    updated_at TIMESTAMP DEFAULT NOW(),
    updated_by INTEGER REFERENCES users(id)
);

-- Work center calendars (working days, shifts, holidays)
CREATE TABLE work_center_calendars (
    id SERIAL PRIMARY KEY,
    work_center_id INTEGER REFERENCES work_centers(id),
    calendar_date DATE NOT NULL,
    shift_1_active BOOLEAN DEFAULT true,
    shift_2_active BOOLEAN DEFAULT true,
    shift_3_active BOOLEAN DEFAULT true,
    is_holiday BOOLEAN DEFAULT false,
    notes TEXT,
    UNIQUE(work_center_id, calendar_date)
);
```

## Indexes for Performance

```sql
-- Core business indexes
CREATE INDEX idx_operations_work_order ON operations(work_order_id);
CREATE INDEX idx_operations_work_center ON operations(work_center_id);
CREATE INDEX idx_operations_status ON operations(status);

-- Scheduling indexes
CREATE INDEX idx_schedule_entries_scenario ON schedule_entries(scenario_id);
CREATE INDEX idx_schedule_entries_work_center ON schedule_entries(work_center_id);
CREATE INDEX idx_schedule_entries_planned_start ON schedule_entries(planned_start);

-- Date-based optimization indexes
CREATE INDEX idx_work_orders_datum_isporuke ON work_orders(datum_isporuke);
CREATE INDEX idx_work_orders_datum_sastavljanja ON work_orders(datum_sastavljanja);
CREATE INDEX idx_work_orders_priority ON work_orders(priority_level DESC);

-- Audit and tracking indexes
CREATE INDEX idx_audit_log_table_record ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_log_user_time ON audit_log(user_id, created_at);
CREATE INDEX idx_operation_timestamps_operation ON operation_timestamps(operation_id);
```

## Migration Strategy

### Phase 1: Core Tables
1. Create organizational structure (organizations, plants, work_centers)
2. Create product hierarchy (products, product_routings)
3. Migrate existing data from SQLite

### Phase 2: Operations & Scheduling
1. Create work_orders and operations tables
2. Set up scheduling system (scenarios, entries)
3. Implement basic scheduling logic

### Phase 3: Advanced Features
1. Add real-time tracking (timestamps, status_log)
2. Implement full audit system
3. Add configuration and calendar management

## Extensibility Features

### Custom Attributes System
```sql
-- Custom attribute definitions
CREATE TABLE custom_attributes (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL, -- 'PRODUCT', 'WORK_CENTER', 'OPERATION'
    attribute_name VARCHAR(100) NOT NULL,
    attribute_type VARCHAR(20) NOT NULL, -- 'TEXT', 'NUMBER', 'DATE', 'BOOLEAN'
    is_required BOOLEAN DEFAULT false,
    default_value TEXT,
    validation_rules JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(entity_type, attribute_name)
);

-- Custom attribute values
CREATE TABLE custom_attribute_values (
    id SERIAL PRIMARY KEY,
    attribute_id INTEGER REFERENCES custom_attributes(id),
    entity_id INTEGER NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    attribute_value TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(attribute_id, entity_id, entity_type)
);
```

### Example BOM Structure
Your example: Product → AS1, AS2, C1, C2, C3 where AS1 → AS3, AS4, C4, C5, C1
```sql
-- Insert product types
INSERT INTO product_types VALUES 
(1, 'PRODUCT', 'Final Product', 'Top level product', true, 1),
(2, 'ASSEMBLY', 'Assembly', 'Sub-assembly component', true, 2),
(3, 'COMPONENT', 'Component', 'Basic component', false, 3);

-- Insert products
INSERT INTO products VALUES 
(1, 'PROD001', 1, 'Main Product', 'Top level product'),
(2, 'AS1', 2, 'Assembly 1', 'First assembly'),
(3, 'AS2', 2, 'Assembly 2', 'Second assembly'),
(4, 'AS3', 2, 'Assembly 3', 'Sub-assembly of AS1'),
(5, 'AS4', 2, 'Assembly 4', 'Sub-assembly of AS1'),
(6, 'C1', 3, 'Component 1', 'Shared component'),
(7, 'C2', 3, 'Component 2', 'Basic component'),
(8, 'C3', 3, 'Component 3', 'Basic component'),
(9, 'C4', 3, 'Component 4', 'Basic component'),
(10, 'C5', 3, 'Component 5', 'Basic component');

-- BOM structure
INSERT INTO bom_structure VALUES 
-- Level 1: Product → Assemblies & Components
(1, 1, 2, 1.0, 1, 1), -- PROD001 → AS1
(2, 1, 3, 1.0, 1, 2), -- PROD001 → AS2
(3, 1, 6, 1.0, 1, 3), -- PROD001 → C1
(4, 1, 7, 2.0, 1, 4), -- PROD001 → C2 (qty 2)
(5, 1, 8, 1.0, 1, 5), -- PROD001 → C3
-- Level 2: AS1 → Sub-assemblies & Components
(6, 2, 4, 1.0, 2, 1), -- AS1 → AS3
(7, 2, 5, 1.0, 2, 2), -- AS1 → AS4
(8, 2, 9, 3.0, 2, 3), -- AS1 → C4 (qty 3)
(9, 2, 10, 1.0, 2, 4), -- AS1 → C5
(10, 2, 6, 2.0, 2, 5); -- AS1 → C1 (qty 2, shared component)
```

## Key Design Benefits

1. **Scalability**: Supports multiple plants, work centers, unlimited product hierarchy levels
2. **Flexibility**: JSONB fields for complex data, configurable hierarchies, custom attributes
3. **BOM Complexity**: Handles shared components, multi-level assemblies, quantity requirements
4. **Work Center Management**: Categories, substitutions, cost tracking, flexible attributes
5. **Audit Trail**: Complete tracking of all changes with full context
6. **Performance**: Proper indexing for large datasets, hierarchy path optimization
7. **Real-time**: Built-in support for operation tracking and timestamps
8. **Multi-level Planning**: Separate scenarios for different planning levels
9. **Extensibility**: Custom attributes system for future requirements

## Implementation Strategy

### Phase 1: MVP (4 weeks)
- Core tables: organizations, plants, work_centers, products, work_orders, operations
- Basic CRUD operations and simple scheduling
- Migrate your current 4,706 operations

### Phase 2: Enhanced Features (4-6 weeks)
- BOM structure and product hierarchy
- Work center substitutions and categories
- Advanced scheduling scenarios

### Phase 3: Enterprise Features (6-8 weeks)
- Full audit system and real-time tracking
- Custom attributes system
- Advanced reporting and analytics

This design can handle your current 4,706 operations and scale to enterprise levels with thousands of work centers, complex multi-level BOMs, and millions of operations.