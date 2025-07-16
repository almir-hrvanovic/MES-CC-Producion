# Implementation Plan - MES Production Scheduling System

## Phase 1: Backend Foundation & Database Setup

- [x] 1. Set up FastAPI project structure and development environment




  - Create backend directory structure with app, models, schemas, api, services folders
  - Set up virtual environment and install core dependencies (FastAPI, SQLAlchemy, psycopg2)
  - Configure development environment with hot reload and debugging
  - _Requirements: 5.1, 5.2_

- [ ] 2. Create PostgreSQL database schema and migration system
  - Design and implement work_orders table with all required fields (kpl, rn, wc, naziv, etc.)
  - Create schedule_entries table for tracking scheduling sequences
  - Set up Alembic for database migrations and version control
  - Create optimized indexes for performance (kpl, rn, wc, dates)
  - _Requirements: 5.1, 5.2, 5.3_

- [ ] 3. Implement data migration from SQLite to PostgreSQL
  - Create migration script to transfer data from legacy-analysis/RawData/queryX.db
  - Validate data integrity and relationships during migration
  - Implement data validation and constraint checking
  - _Requirements: 5.1, 5.2, 5.4_

- [ ] 4. Create core data models and database connection
  - Implement SQLAlchemy models for WorkOrder, ScheduleEntry, WorkCenter
  - Set up database connection pooling and session management
  - Create base repository pattern for data access
  - _Requirements: 5.1, 5.2_

## Phase 2: Core API Development & Business Logic

- [ ] 5. Implement Work Orders CRUD API endpoints
  - Create GET /api/work-orders with filtering by work center, status, urgency
  - Implement POST /api/work-orders for creating new work orders
  - Add PUT /api/work-orders/{id} for updating work order details
  - Create PATCH /api/work-orders/{id}/status for status changes
  - _Requirements: 1.1, 1.2, 3.1, 3.2_

- [ ] 6. Develop date-based optimization algorithms
  - Implement sorting by datum_isporuke (delivery date) with proper date handling
  - Create sorting by datum_sastavljanja (assembly date) functionality
  - Add support for other date field optimization options
  - Implement urgency-based prioritization using HITNO field values
  - _Requirements: 1.2, 1.3, 1.4, 7.2, 7.3_

- [ ] 7. Create scheduling service with conflict detection
  - Implement POST /api/schedule/optimize endpoint for date-based optimization
  - Create PUT /api/schedule/reorder for handling drag-drop sequence changes
  - Develop conflict detection logic for overlapping schedules and capacity issues
  - Add time calculation service for estimated start/end times
  - _Requirements: 1.4, 1.5, 2.3, 2.6_

- [ ] 8. Implement work center management functionality
  - Create GET /api/work-centers endpoint for SAV100 and G1000 data
  - Add work center filtering and capacity calculation logic
  - Implement cross-work center dependency handling for multi-WC work orders
  - Create work center specific scheduling optimization
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

## Phase 3: Frontend Development & User Interface

- [ ] 9. Set up React project with TypeScript and essential dependencies
  - Initialize React 18 project with TypeScript configuration
  - Install and configure Tailwind CSS for styling
  - Set up React Router for navigation between work centers
  - Install drag-drop library (@dnd-kit/core) and date handling (date-fns)
  - _Requirements: 6.1, 6.5_

- [ ] 10. Create work order management interface
  - Build WorkOrderList component with filtering and search functionality
  - Implement work order creation form with all required fields
  - Add work order status management with mark-as-finished functionality
  - Create bulk operations for marking multiple orders as finished
  - _Requirements: 1.1, 3.1, 3.2, 3.6_

- [ ] 11. Implement optimization controls and date-based sorting
  - Create OptimizationControls component with date criteria selection
  - Add optimization trigger buttons for different date fields
  - Implement loading states and progress indicators during optimization
  - Display optimization results with total count and timeline estimates
  - _Requirements: 1.2, 1.3, 1.4, 1.5_

- [ ] 12. Build drag-and-drop scheduling interface
  - Create SchedulingGrid component with draggable work order cards
  - Implement drag-drop functionality with visual feedback and animations
  - Add real-time sequence reordering with immediate visual updates
  - Create conflict highlighting and resolution suggestions
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.6_

## Phase 4: Advanced Features & Real-time Updates

- [ ] 13. Implement work center tabs and filtering
  - Create WorkCenterTabs component for switching between SAV100 and G1000
  - Add work center specific views with filtered work orders
  - Implement capacity display and workload visualization for each center
  - Create work center performance metrics and statistics
  - _Requirements: 4.1, 4.2, 4.5_

- [ ] 14. Add urgent order highlighting and prioritization
  - Implement visual highlighting for work orders with HITNO > 0
  - Create urgent order filtering and dedicated urgent orders view
  - Add priority-based sorting integration with optimization algorithms
  - Implement urgent order notifications and alerts
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 15. Implement real-time updates with WebSocket connections
  - Set up WebSocket server endpoints for live schedule updates
  - Create WebSocket client connection management in React
  - Implement real-time broadcasting of schedule changes across users
  - Add connection status indicators and automatic reconnection logic
  - _Requirements: 6.3, 2.5_

- [ ] 16. Create responsive design and cross-browser compatibility
  - Implement responsive layouts for different screen sizes and devices
  - Test and optimize for Chrome, Firefox, and Edge browsers
  - Add mobile-friendly touch interactions for drag-drop on tablets
  - Implement accessibility features and keyboard navigation support
  - _Requirements: 6.1, 6.5_

## Phase 5: Testing, Optimization & Deployment

- [ ] 17. Implement comprehensive testing suite
  - Create unit tests for all backend services and API endpoints using pytest
  - Add frontend component tests using Jest and React Testing Library
  - Implement integration tests for drag-drop workflows and optimization
  - Create performance tests for handling 4,706+ operations efficiently
  - _Requirements: 5.3, 6.2_

- [ ] 18. Optimize performance for large datasets
  - Implement virtual scrolling for large work order lists
  - Add database query optimization and proper indexing strategies
  - Create caching layer for frequently accessed optimization results
  - Implement pagination and lazy loading for improved response times
  - _Requirements: 5.3, 6.2_

- [ ] 19. Set up Ubuntu deployment with Nginx configuration
  - Create production deployment scripts and configuration files
  - Set up Nginx reverse proxy with static file serving
  - Configure Gunicorn for Python application server management
  - Implement local network security restrictions and access controls
  - _Requirements: 6.4_

- [ ] 20. Final integration testing and production readiness
  - Perform end-to-end testing of complete workflow from optimization to completion
  - Test concurrent user scenarios with multiple planners using the system
  - Validate data migration integrity and backup/restore procedures
  - Create user documentation and system administration guides
  - _Requirements: 6.2, 6.3, 5.4_