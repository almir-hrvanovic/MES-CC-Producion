# MES Web Application Architecture Analysis

## Current System Analysis
- **Existing**: Excel VBA-based production scheduling system
- **Core Logic**: Complex shift-based scheduling with break management
- **Data**: Work orders, machine calendars, production plans
- **Users**: Local network access only (factory floor)

## Requirements Summary
- **Primary**: Create production orders with date-based optimization
- **Optimization Options**: DatumIsporuke, DatumSastavljanja, DatumTreci, other dates
- **Manual Control**: Drag-drop fine-tuning of schedules
- **Status Management**: Mark projects as finished, remove from optimization
- **Future**: Additional optimization rules to be added
- **Infrastructure**: Ubuntu server with Nginx + PostgreSQL

## Technology Stack Recommendations

### Option 1: Modern Full-Stack (Recommended)
**Frontend**: React + TypeScript
- **Pros**: Excellent drag-drop libraries (react-beautiful-dnd, @dnd-kit)
- **Pros**: Rich scheduling UI components (FullCalendar, react-big-calendar)
- **Pros**: Fast development, great ecosystem
- **Cons**: Learning curve if team unfamiliar

**Backend**: Node.js + Express + TypeScript
- **Pros**: Same language as frontend (JavaScript/TypeScript)
- **Pros**: Fast development, good PostgreSQL integration
- **Pros**: Easy to port VBA logic to JavaScript
- **Cons**: May need performance optimization for complex scheduling

### Option 2: Python-Based (Good Alternative)
**Frontend**: React (same as Option 1)
**Backend**: FastAPI + Python
- **Pros**: Excellent for data processing and optimization algorithms
- **Pros**: Libraries like pandas for data manipulation
- **Pros**: Easy integration with scheduling algorithms
- **Cons**: Two different languages (Python + JavaScript)

### Option 3: PHP-Based (Simplest)
**Frontend**: Vue.js + PHP backend
- **Pros**: Simple deployment on existing LAMP-like stack
- **Pros**: Easy to learn and maintain
- **Cons**: Less modern, fewer scheduling-specific libraries

## Recommended Architecture: Node.js + React

### Backend Structure
```
/backend
├── /src
│   ├── /controllers     # API endpoints
│   ├── /services        # Business logic (scheduling algorithms)
│   ├── /models          # Database models
│   ├── /utils           # Helper functions
│   └── /migrations      # Database schema
├── package.json
└── tsconfig.json
```

### Frontend Structure
```
/frontend
├── /src
│   ├── /components      # Reusable UI components
│   ├── /pages           # Main application pages
│   ├── /services        # API communication
│   ├── /utils           # Helper functions
│   └── /types           # TypeScript type definitions
├── package.json
└── tsconfig.json
```

## Database Schema Design

### Core Tables
```sql
-- Work Orders (Radni Nalozi)
CREATE TABLE work_orders (
    id SERIAL PRIMARY KEY,
    kpl VARCHAR(50) NOT NULL,
    poz VARCHAR(50) NOT NULL,
    naziv VARCHAR(200) NOT NULL,
    duration_minutes INTEGER NOT NULL,
    datum_isporuke DATE,
    datum_sastavljanja DATE,
    datum_treci DATE,
    priority INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending', -- pending, scheduled, in_progress, finished
    machine_id INTEGER REFERENCES machines(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Machines (Mašine)
CREATE TABLE machines (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT true
);

-- Schedule Entries (Raspored)
CREATE TABLE schedule_entries (
    id SERIAL PRIMARY KEY,
    work_order_id INTEGER REFERENCES work_orders(id),
    machine_id INTEGER REFERENCES machines(id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    entry_type VARCHAR(20) NOT NULL, -- 'work', 'break', 'nonwork'
    sequence_order INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Machine Calendar (Kalendar Mašina)
CREATE TABLE machine_calendar (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    machine_id INTEGER REFERENCES machines(id),
    shift_1 VARCHAR(1) DEFAULT 'r', -- 'r' = radna, 'n' = neradna
    shift_2 VARCHAR(1) DEFAULT 'r',
    shift_3 VARCHAR(1) DEFAULT 'r',
    UNIQUE(date, machine_id)
);
```

## Key Features Implementation

### 1. Production Order Creation
```typescript
// API endpoint
POST /api/work-orders
{
  "kpl": "12345",
  "poz": "001",
  "naziv": "Naziv proizvoda",
  "duration_minutes": 120,
  "datum_isporuke": "2025-01-20",
  "priority": 1
}
```

### 2. Date-Based Optimization
```typescript
// API endpoint
POST /api/schedule/optimize
{
  "optimization_type": "datum_isporuke", // or "datum_sastavljanja", "datum_treci"
  "machine_id": 1,
  "start_date": "2025-01-15"
}
```

### 3. Drag-Drop Interface
- Use `@dnd-kit/core` for React drag-drop
- Real-time schedule updates
- Visual feedback during dragging
- Conflict detection and highlighting

### 4. Status Management
```typescript
// Mark as finished
PATCH /api/work-orders/:id
{
  "status": "finished"
}
```

## Development Phases

### Phase 1: Foundation (2-3 weeks)
1. Set up development environment
2. Create database schema
3. Basic CRUD operations for work orders
4. Simple scheduling algorithm (port from VBA)

### Phase 2: Core Features (3-4 weeks)
1. Date-based optimization algorithms
2. Basic drag-drop interface
3. Machine calendar integration
4. Status management

### Phase 3: Advanced Features (2-3 weeks)
1. Advanced drag-drop with conflict detection
2. Real-time updates
3. Reporting and analytics
4. Performance optimization

### Phase 4: Polish & Deploy (1-2 weeks)
1. UI/UX improvements
2. Testing and bug fixes
3. Deployment setup
4. Documentation

## Deployment Architecture

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-local-server;
    
    # Frontend (React build)
    location / {
        root /var/www/mes-app/build;
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Process Management
- Use PM2 for Node.js process management
- PostgreSQL connection pooling
- Log rotation and monitoring

## Migration Strategy

### Data Migration
1. Export current Excel data to CSV
2. Create migration scripts to populate PostgreSQL
3. Validate data integrity
4. Test scheduling algorithms with real data

### User Training
1. Create user documentation
2. Side-by-side testing period
3. Gradual transition from Excel to web app

## Estimated Timeline
- **Total Development**: 8-12 weeks
- **Testing & Deployment**: 2-3 weeks
- **User Training**: 1-2 weeks

## Next Steps
1. Confirm technology stack choice
2. Set up development environment
3. Create detailed database schema
4. Start with basic CRUD operations
5. Port core scheduling logic from VBA

---

*Created: January 2025*
*Status: Architecture Planning*