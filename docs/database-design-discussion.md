# Database Design Discussion - MES Production Scheduling System

## Discussion Date: January 16, 2025

## Context
This document captures the key decisions and requirements discussed during the database design phase for the MES Production Scheduling System.

## Key Requirements Identified

### 1. Normalized Database Structure
- **Decision**: Use normalized approach with multiple tables
- **Reason**: Better data integrity, scalability, and future expansion
- **Impact**: Supports enterprise-level growth and complex relationships

### 2. Multi-Level Product Hierarchy
- **Requirement**: Support complex BOM structures beyond simple 3-level hierarchy
- **Example Structure**: 
  ```
  Product (top level)
  ├── Assembly 1 (AS1)
  │   ├── Sub-assembly 3 (AS3)
  │   ├── Sub-assembly 4 (AS4)
  │   ├── Component 4 (C4)
  │   ├── Component 5 (C5)
  │   └── Component 1 (C1) - shared component
  ├── Assembly 2 (AS2)
  ├── Component 1 (C1) - shared component
  ├── Component 2 (C2)
  └── Component 3 (C3)
  ```
- **Solution**: Flexible BOM structure with parent-child relationships and quantity requirements

### 3. Enterprise-Level Planning Support
- **Requirement**: Support plant floor, mid-level, and high-level planning
- **Solution**: Multi-scenario scheduling system with different planning levels
- **Future Scope**: Multiple plants, organizations, and complex hierarchies

### 4. Complete Audit Trail
- **Requirement**: Track all changes with full context
- **Details Needed**:
  - User identification
  - Session tracking
  - IP addresses and workstation names
  - Change reasons
  - Timestamps for all modifications
- **Solution**: Comprehensive audit_log table with JSONB for flexible data storage

### 5. Real-time Operation Tracking
- **Requirement**: System to register operation start/stop timestamps
- **Features**:
  - Unique operation identification
  - Workstation and operator tracking
  - Multiple timestamp types (START, STOP, PAUSE, RESUME)
- **Solution**: operation_timestamps table with flexible tracking capabilities

### 6. Work Center Management
- **Current State**: 2 work centers (SAV100, G1000)
- **Future Requirements**:
  - Multiple work center categories (to be defined later)
  - Work center substitutions for flexibility
  - Cost tracking per work center
  - Setup times and capacity management
- **Solution**: Flexible work center categories with substitution support

### 7. Extensibility Requirements
- **Need**: Ability to add more dimensions and data types without schema changes
- **Solution**: 
  - JSONB fields for flexible attributes
  - Custom attributes system
  - Configurable product types and work center categories

## Database Design Decisions

### Core Architecture
- **Organizations** → **Plants** → **Work Centers** → **Operations**
- **Products** with flexible hierarchy via BOM structure
- **Scheduling Scenarios** for different planning levels
- **Complete Audit System** for all changes

### Key Tables Structure
1. **Organizational**: organizations, plants, work_centers, work_center_categories
2. **Product Management**: products, product_types, bom_structure, bom_hierarchy_paths
3. **Operations**: work_orders, operations, product_routings
4. **Scheduling**: scheduling_scenarios, schedule_entries, schedule_history
5. **Tracking**: operation_timestamps, operation_status_log
6. **Audit**: audit_log, user_sessions, users
7. **Configuration**: system_config, work_center_calendars, custom_attributes

### Flexibility Features
- **JSONB Fields**: For specifications, cost data, dependencies, and custom attributes
- **Custom Attributes System**: Add fields to any entity without schema changes
- **Work Center Substitutions**: Alternative work centers with time/cost factors
- **BOM Hierarchy Paths**: Optimized lookups for complex product structures

## Implementation Strategy

### ✅ Phase 1: MVP Foundation (Week 1 - COMPLETED)
- ✅ Project structure and organization
- ✅ Enterprise database schema design
- ✅ FastAPI backend structure with API endpoints
- ✅ Kiro specs (requirements, design, tasks)
- ✅ Complete documentation

### 🔄 Phase 1 Continuation (Week 1-2 - IN PROGRESS)
- 🔄 PostgreSQL database schema creation (Task 2)
- ⏳ Data migration from existing SQLite database (Task 3)
- ⏳ Core database operations (Task 4)

### ⏳ Phase 2: Core Development (Week 2-3)
- API development and business logic (Tasks 5-8)
- React frontend development (Tasks 9-12)
- Basic scheduling functionality

### ⏳ Phase 3: Advanced Features (Week 3-4)
- Advanced scheduling and drag-drop (Tasks 13-16)
- Testing and optimization (Tasks 17-18)
- Deployment and production readiness (Tasks 19-20)

## Technical Considerations

### Performance Optimization
- Proper indexing strategy for large datasets
- BOM hierarchy path optimization for quick lookups
- JSONB indexing for flexible attributes
- Connection pooling for concurrent users

### Scalability Features
- Support for multiple plants and organizations
- Unlimited product hierarchy levels
- Configurable work center types
- Extensible audit system

### Data Integrity
- Foreign key constraints for referential integrity
- Unique constraints for business rules
- Check constraints for data validation
- Transaction management for complex operations

## Migration Considerations

### Current Data (SQLite)
- **4,706 manufacturing operations**
- **599 unique products (KPL)**
- **1,746 work orders (RN)**
- **2 work centers**: SAV100 (Press), G1000 (CNC)
- **Date range**: December 2024 - September 2025

### Migration Strategy
1. Create core PostgreSQL schema
2. Migrate organizational structure (plants, work centers)
3. Migrate product data with basic hierarchy
4. Migrate work orders and operations
5. Create initial scheduling scenarios
6. Validate data integrity and relationships

## Future Considerations

### Planned Enhancements
- Integration with ERP systems
- Advanced optimization algorithms
- Machine learning for predictive scheduling
- Mobile applications for shop floor
- Integration with IoT sensors and equipment

### Extensibility Points
- Custom workflow definitions
- Configurable business rules
- Plugin architecture for custom modules
- API integration capabilities

## Conclusion

The database design provides a solid foundation for enterprise-level MES implementation while maintaining flexibility for future growth. The normalized structure supports complex manufacturing scenarios while the audit system ensures complete traceability. The phased implementation approach allows for incremental development and validation.

---

**Current Status**: Task 1 ✅ COMPLETED - FastAPI backend structure implemented
**Next Steps**: Task 2 - Create PostgreSQL database schema and migration system

**Key Success Factors**:
- ✅ Project structure and backend foundation established
- ✅ Enterprise database design completed
- 🔄 PostgreSQL schema creation in progress
- ⏳ Data migration planning
- ⏳ Performance optimization implementation