# Design Document - MES Production Scheduling System

## Overview

The MES Production Scheduling System is designed as a modern web application using React frontend with Python FastAPI backend, connected to PostgreSQL database. The system architecture follows a RESTful API pattern with real-time updates for collaborative scheduling. The design leverages the existing data structure analysis (KPL + RN + WC hierarchy) and provides intuitive drag-drop interfaces for production planning.

## Architecture

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Client  │    │  FastAPI Server │    │  PostgreSQL DB  │
│                 │    │                 │    │                 │
│ - Scheduling UI │◄──►│ - REST APIs     │◄──►│ - Work Orders   │
│ - Drag & Drop   │    │ - Business Logic│    │ - Schedules     │
│ - Real-time     │    │ - Optimization  │    │ - Machine Data  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Ubuntu + Nginx  │
                    │ - Reverse Proxy │
                    │ - Static Files  │
                    │ - Load Balancer │
                    └─────────────────┘
```

### Technology Stack
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Backend**: Python 3.12 + FastAPI + SQLAlchemy
- **Database**: PostgreSQL 15+ with optimized indexes
- **Deployment**: Ubuntu Server + Nginx + Gunicorn
- **Real-time**: WebSocket connections for live updates

## Components and Interfaces

### Frontend Components

#### 1. WorkOrderManager Component
```typescript
interface WorkOrderManagerProps {
  workOrders: WorkOrder[];
  onOptimize: (criteria: OptimizationCriteria) => void;
  onStatusChange: (id: number, status: WorkOrderStatus) => void;
}
```
**Responsibilities:**
- Display work order list with filtering and sorting
- Handle optimization criteria selection
- Manage work order status changes
- Integrate with drag-drop scheduling

#### 2. SchedulingGrid Component
```typescript
interface SchedulingGridProps {
  schedule: ScheduleEntry[];
  workCenter: WorkCenter;
  onReorder: (newOrder: ScheduleEntry[]) => void;
  onConflictDetected: (conflicts: ScheduleConflict[]) => void;
}
```
**Responsibilities:**
- Render draggable schedule timeline
- Handle drag-drop reordering operations
- Detect and highlight scheduling conflicts
- Calculate time estimates and dependencies

#### 3. WorkCenterTabs Component
```typescript
interface WorkCenterTabsProps {
  workCenters: WorkCenter[];
  activeCenter: string;
  onCenterChange: (centerId: string) => void;
}
```
**Responsibilities:**
- Switch between SAV100 and G1000 work centers
- Display work center specific metrics
- Filter operations by selected work center

#### 4. OptimizationControls Component
```typescript
interface OptimizationControlsProps {
  criteria: OptimizationCriteria[];
  onOptimize: (selected: OptimizationCriteria) => void;
  isOptimizing: boolean;
}
```
**Responsibilities:**
- Provide date-based optimization options
- Trigger optimization algorithms
- Display optimization progress and results

### Backend API Design

#### 1. Work Orders API
```python
# GET /api/work-orders
# Query parameters: work_center, status, urgent_only, limit, offset
class WorkOrderListResponse(BaseModel):
    work_orders: List[WorkOrder]
    total_count: int
    work_center_stats: Dict[str, int]

# POST /api/work-orders/{id}/status
class StatusUpdateRequest(BaseModel):
    status: WorkOrderStatus
    completed_at: Optional[datetime] = None
```

#### 2. Scheduling API
```python
# POST /api/schedule/optimize
class OptimizationRequest(BaseModel):
    work_center: str
    criteria: OptimizationCriteria  # datum_isporuke, datum_sastavljanja, etc.
    work_order_ids: Optional[List[int]] = None

class OptimizationResponse(BaseModel):
    optimized_schedule: List[ScheduleEntry]
    estimated_completion: datetime
    conflicts: List[ScheduleConflict]

# PUT /api/schedule/reorder
class ReorderRequest(BaseModel):
    work_center: str
    new_order: List[int]  # work_order_ids in new sequence
```

#### 3. Real-time WebSocket API
```python
# WebSocket /ws/schedule/{work_center}
class ScheduleUpdateMessage(BaseModel):
    type: str  # "reorder", "status_change", "optimization_complete"
    work_center: str
    data: Dict[str, Any]
    timestamp: datetime
```

### Backend Services

#### 1. SchedulingService
```python
class SchedulingService:
    def optimize_by_date(self, criteria: OptimizationCriteria, work_center: str) -> List[ScheduleEntry]
    def reorder_schedule(self, work_center: str, new_order: List[int]) -> List[ScheduleEntry]
    def detect_conflicts(self, schedule: List[ScheduleEntry]) -> List[ScheduleConflict]
    def calculate_completion_times(self, schedule: List[ScheduleEntry]) -> Dict[int, datetime]
```

#### 2. WorkOrderService
```python
class WorkOrderService:
    def get_work_orders(self, filters: WorkOrderFilters) -> List[WorkOrder]
    def update_status(self, work_order_id: int, status: WorkOrderStatus) -> WorkOrder
    def get_urgent_orders(self, work_center: str) -> List[WorkOrder]
    def bulk_status_update(self, work_order_ids: List[int], status: WorkOrderStatus) -> int
```

#### 3. WebSocketManager
```python
class WebSocketManager:
    def broadcast_schedule_update(self, work_center: str, update: ScheduleUpdateMessage)
    def notify_optimization_complete(self, work_center: str, result: OptimizationResponse)
    def handle_client_connection(self, websocket: WebSocket, work_center: str)
```

## Data Models

### Core Data Models
```python
class WorkOrder(BaseModel):
    id: int
    kpl: int  # Product identifier
    rn: int   # Work order number
    wc: str   # Work center (SAV100, G1000)
    naziv: str
    norma: float  # Duration in hours
    quantity: int
    datum_isporuke: Optional[date]
    datum_sastavljanja: Optional[date]
    hitno: int  # Urgency level
    status: WorkOrderStatus
    created_at: datetime
    updated_at: datetime

class ScheduleEntry(BaseModel):
    id: int
    work_order_id: int
    work_center: str
    sequence_order: int
    estimated_start: datetime
    estimated_end: datetime
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]

class WorkCenter(BaseModel):
    code: str  # SAV100, G1000
    name: str
    description: str
    capacity_hours_per_day: float
    is_active: bool
```

### Optimization Models
```python
class OptimizationCriteria(str, Enum):
    DATUM_ISPORUKE = "datum_isporuke"
    DATUM_SASTAVLJANJA = "datum_sastavljanja"
    HITNO_PRIORITY = "hitno"
    CUSTOM_ORDER = "custom"

class ScheduleConflict(BaseModel):
    work_order_id: int
    conflict_type: str  # "overlap", "capacity_exceeded", "dependency_violation"
    description: str
    suggested_resolution: str
```

## Error Handling

### Frontend Error Handling
- **Network Errors**: Retry mechanism with exponential backoff
- **Validation Errors**: Real-time form validation with user-friendly messages
- **Drag-Drop Errors**: Revert to previous state with error notification
- **WebSocket Disconnection**: Automatic reconnection with status indicator

### Backend Error Handling
- **Database Errors**: Transaction rollback with detailed logging
- **Optimization Failures**: Fallback to previous schedule with error reporting
- **Concurrent Updates**: Optimistic locking with conflict resolution
- **API Rate Limiting**: Request throttling with appropriate HTTP status codes

## Testing Strategy

### Frontend Testing
- **Unit Tests**: Jest + React Testing Library for component logic
- **Integration Tests**: Cypress for end-to-end drag-drop workflows
- **Performance Tests**: Lighthouse audits for loading and interaction times
- **Accessibility Tests**: axe-core for WCAG compliance

### Backend Testing
- **Unit Tests**: pytest for service layer and business logic
- **API Tests**: FastAPI TestClient for endpoint validation
- **Database Tests**: pytest-postgresql for data integrity
- **Load Tests**: locust for concurrent user simulation

### Integration Testing
- **WebSocket Tests**: Real-time update synchronization
- **Optimization Tests**: Algorithm accuracy with production data
- **Cross-browser Tests**: Selenium grid for browser compatibility
- **Database Migration Tests**: Schema changes and data preservation

## Performance Considerations

### Frontend Optimization
- **Virtual Scrolling**: Handle large work order lists (4,706+ items)
- **Memoization**: React.memo for expensive component renders
- **Code Splitting**: Lazy loading for work center specific components
- **Caching**: React Query for API response caching

### Backend Optimization
- **Database Indexing**: Optimized indexes for KPL, RN, WC, and date fields
- **Query Optimization**: SQLAlchemy query optimization with EXPLAIN ANALYZE
- **Connection Pooling**: PostgreSQL connection pool management
- **Caching Layer**: Redis for frequently accessed optimization results

### Real-time Performance
- **WebSocket Throttling**: Batch updates to prevent message flooding
- **Selective Updates**: Send only changed data, not full schedules
- **Client-side Debouncing**: Prevent excessive API calls during drag operations
- **Background Processing**: Async optimization calculations

## Security Considerations

### Authentication & Authorization
- **Local Network Only**: IP-based access restriction
- **Session Management**: Secure session tokens with expiration
- **Role-based Access**: Different permissions for planners vs supervisors
- **API Security**: Rate limiting and input validation

### Data Protection
- **SQL Injection Prevention**: Parameterized queries with SQLAlchemy
- **XSS Protection**: Content Security Policy and input sanitization
- **CSRF Protection**: CSRF tokens for state-changing operations
- **Data Validation**: Pydantic models for request/response validation

## Deployment Architecture

### Production Environment
```
Internet ──X──► [Firewall] ──► [Nginx] ──► [Gunicorn] ──► [FastAPI App]
                    │              │           │              │
                    │              │           │              ▼
                    │              │           │         [PostgreSQL]
                    │              │           │              │
                    │              ▼           ▼              │
                    │         [Static Files] [Logs]          │
                    │              │           │              │
                    ▼              ▼           ▼              ▼
              [Local Network] [React Build] [System Logs] [Data Backup]
```

### Monitoring & Logging
- **Application Logs**: Structured logging with correlation IDs
- **Performance Metrics**: Response times and resource usage
- **Error Tracking**: Centralized error collection and alerting
- **Health Checks**: Automated system health monitoring