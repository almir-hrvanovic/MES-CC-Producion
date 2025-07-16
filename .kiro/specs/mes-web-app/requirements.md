# Requirements Document - MES Production Scheduling System

## Introduction

The MES Production Scheduling System is a modern web-based application designed to replace the existing Excel VBA-based production planning system. The system will provide manufacturing companies with efficient production scheduling, work order management, and real-time status tracking capabilities. The application will handle 4,706+ manufacturing operations across multiple work centers with date-based optimization and drag-drop scheduling interface.

## Requirements

### Requirement 1

**User Story:** As a production planner, I want to create and manage work orders with date-based optimization, so that I can efficiently schedule production based on delivery dates and assembly requirements.

#### Acceptance Criteria

1. WHEN a user accesses the work order creation interface THEN the system SHALL display a form with fields for KPL, RN, NAZIV, work center, duration, and date fields
2. WHEN a user selects optimization by "DatumIsporuke" THEN the system SHALL sort all pending work orders by delivery date in ascending order
3. WHEN a user selects optimization by "DatumSastavljanja" THEN the system SHALL sort all pending work orders by assembly date in ascending order
4. WHEN a user selects optimization by other available date fields THEN the system SHALL sort work orders accordingly and display the optimized sequence
5. WHEN work orders are optimized THEN the system SHALL display the total count of operations and estimated completion timeline

### Requirement 2

**User Story:** As a production supervisor, I want to fine-tune the optimized schedule using drag-and-drop functionality, so that I can manually adjust the sequence based on shop floor conditions and priorities.

#### Acceptance Criteria

1. WHEN a user views the optimized schedule THEN the system SHALL display work orders in a draggable list or grid format
2. WHEN a user drags a work order to a new position THEN the system SHALL update the sequence order in real-time
3. WHEN a work order is moved THEN the system SHALL recalculate affected start and end times for subsequent operations
4. WHEN drag-drop operations occur THEN the system SHALL provide visual feedback during the drag operation
5. WHEN sequence changes are made THEN the system SHALL automatically save the new order and update the database
6. WHEN conflicts arise from reordering THEN the system SHALL highlight potential scheduling conflicts

### Requirement 3

**User Story:** As a production manager, I want to mark projects as finished and remove them from active scheduling, so that completed work doesn't interfere with current production planning.

#### Acceptance Criteria

1. WHEN a user views active work orders THEN the system SHALL provide a "Mark as Finished" action for each work order
2. WHEN a user marks a work order as finished THEN the system SHALL change its status to "completed" in the database
3. WHEN work orders are marked as finished THEN the system SHALL remove them from the active scheduling view
4. WHEN filtering options are available THEN the system SHALL allow users to view completed work orders separately
5. WHEN a work order is marked finished THEN the system SHALL update capacity calculations and available time slots
6. WHEN bulk operations are needed THEN the system SHALL allow marking multiple work orders as finished simultaneously

### Requirement 4

**User Story:** As a production planner, I want to manage work orders across different work centers (SAV100 and G1000), so that I can optimize scheduling for each machine type independently.

#### Acceptance Criteria

1. WHEN a user accesses the scheduling interface THEN the system SHALL display separate views for each work center (SAV100, G1000)
2. WHEN filtering by work center THEN the system SHALL show only operations assigned to the selected work center
3. WHEN optimizing schedules THEN the system SHALL consider work center capacity and capabilities
4. WHEN work orders span multiple work centers THEN the system SHALL handle cross-work center dependencies
5. WHEN viewing work center status THEN the system SHALL display current workload and available capacity for each machine

### Requirement 5

**User Story:** As a system administrator, I want the application to handle the existing data structure (4,706 operations, 599 products, 1,746 work orders), so that we can migrate from the current Excel system without data loss.

#### Acceptance Criteria

1. WHEN the system starts THEN it SHALL successfully connect to PostgreSQL database with migrated production data
2. WHEN displaying work orders THEN the system SHALL handle the KPL + RN + WC unique identifier structure
3. WHEN processing large datasets THEN the system SHALL maintain response times under 2 seconds for typical operations
4. WHEN data integrity is required THEN the system SHALL validate all work order relationships and constraints
5. WHEN historical data is accessed THEN the system SHALL preserve all original Excel data fields and relationships

### Requirement 6

**User Story:** As a production team member, I want to access the system through a web browser on the local network, so that multiple users can collaborate on production scheduling from different workstations.

#### Acceptance Criteria

1. WHEN users access the application URL THEN the system SHALL load the web interface in modern browsers (Chrome, Firefox, Edge)
2. WHEN multiple users access simultaneously THEN the system SHALL support concurrent user sessions without conflicts
3. WHEN real-time updates occur THEN the system SHALL reflect changes across all active user sessions
4. WHEN the system is deployed THEN it SHALL be accessible only within the local network for security
5. WHEN users interact with the interface THEN the system SHALL provide responsive design for different screen sizes

### Requirement 7

**User Story:** As a production planner, I want to view urgent orders (HITNO priority) with special highlighting, so that critical deliveries are prioritized in the scheduling process.

#### Acceptance Criteria

1. WHEN displaying work orders THEN the system SHALL visually highlight orders with HITNO values greater than 0
2. WHEN optimizing schedules THEN the system SHALL consider urgency levels in the sorting algorithm
3. WHEN urgent orders exist THEN the system SHALL display them prominently in the interface
4. WHEN filtering options are used THEN the system SHALL allow filtering by urgency level
5. WHEN urgent orders are scheduled THEN the system SHALL ensure they receive priority placement in the timeline