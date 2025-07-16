# MES Production Scheduler - Project Overview

## Business Context
Manufacturing company transitioning from Excel VBA-based production scheduling to modern web application.

## Current System Analysis
- **Legacy System**: Excel VBA with complex shift-based scheduling
- **Data Volume**: 4,706 manufacturing operations across 599 products
- **Work Centers**: SAV100 (Press Brake), G1000 (CNC Milling)
- **Scheduling Logic**: 3-shift system with break management

## Target System Requirements
1. **Date-based Optimization**: Sort by delivery dates, assembly dates, etc.
2. **Manual Fine-tuning**: Drag-drop interface for schedule adjustments
3. **Status Management**: Mark projects as finished, remove from planning
4. **Real-time Updates**: Live schedule modifications
5. **Multi-work Center**: Support for different machine types

## Technical Architecture
- **Frontend**: React + TypeScript for rich UI interactions
- **Backend**: Python FastAPI for data processing and scheduling algorithms
- **Database**: PostgreSQL for production data storage
- **Deployment**: Ubuntu server with Nginx (local network only)

## Development Approach
- **MVP First**: 4-week timeline for core functionality
- **Iterative Enhancement**: Add advanced features post-MVP
- **Data Migration**: Preserve existing production data
- **Parallel Operation**: Run alongside Excel system during transition

## Success Metrics
- **Functionality**: All core scheduling features working
- **Performance**: Sub-second response for schedule optimization
- **Usability**: Intuitive drag-drop interface
- **Reliability**: 99%+ uptime for production environment

## Risk Mitigation
- **Data Backup**: Multiple backups of production data
- **Gradual Migration**: Phased transition from Excel
- **User Training**: Documentation and training materials
- **Rollback Plan**: Ability to return to Excel system if needed