# Technology Stack Decision - MES Web Application

## Final Technology Choice: React + Python

### Frontend: React + TypeScript
**Why React:**
- Excellent drag-drop libraries (@dnd-kit, react-beautiful-dnd)
- Rich scheduling UI components (FullCalendar, react-big-calendar)
- Large ecosystem and community support
- Perfect for complex manufacturing interfaces

### Backend: Python + FastAPI
**Why Python:**
- **Data Processing**: Pandas for complex data manipulation
- **Scheduling Algorithms**: Easy to port VBA logic to Python
- **Database**: SQLAlchemy ORM for PostgreSQL
- **Performance**: Fast enough for your local network requirements
- **Libraries**: Rich ecosystem for optimization (scipy, numpy)

### Database: PostgreSQL
**Why PostgreSQL:**
- Already running on your Ubuntu server
- Excellent for complex queries and scheduling data
- JSON support for flexible configuration
- Strong performance for manufacturing data

### Deployment: Ubuntu + Nginx
- **Nginx**: Reverse proxy and static file serving
- **Gunicorn**: Python WSGI server
- **PM2 or Systemd**: Process management
- **Local Network**: Perfect for factory floor access

## Project Structure

```
mes-web-app/
├── backend/                        # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI application
│   │   ├── models/                # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── work_order.py
│   │   │   ├── machine.py
│   │   │   └── schedule.py
│   │   ├── schemas/               # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── work_order.py
│   │   │   └── schedule.py
│   │   ├── api/                   # API routes
│   │   │   ├── __init__.py
│   │   │   ├── work_orders.py
│   │   │   ├── scheduling.py
│   │   │   └── machines.py
│   │   ├── services/              # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── scheduler.py       # Main scheduling engine
│   │   │   ├── optimizer.py       # Date-based optimization
│   │   │   └── shift_manager.py   # Shift and break logic
│   │   ├── database/              # Database configuration
│   │   │   ├── __init__.py
│   │   │   ├── connection.py
│   │   │   └── migrations/
│   │   └── utils/                 # Helper functions
│   │       ├── __init__.py
│   │       └── date_utils.py
│   ├── requirements.txt
│   ├── alembic.ini               # Database migrations
│   └── .env                      # Environment variables
│
├── frontend/                      # React TypeScript frontend
│   ├── public/
│   ├── src/
│   │   ├── components/           # Reusable components
│   │   │   ├── common/
│   │   │   ├── scheduling/
│   │   │   │   ├── ScheduleGrid.tsx
│   │   │   │   ├── DragDropSchedule.tsx
│   │   │   │   └── WorkOrderCard.tsx
│   │   │   └── forms/
│   │   ├── pages/                # Main application pages
│   │   │   ├── Dashboard.tsx
│   │   │   ├── WorkOrders.tsx
│   │   │   ├── Scheduling.tsx
│   │   │   └── Machines.tsx
│   │   ├── services/             # API communication
│   │   │   ├── api.ts
│   │   │   ├── workOrderService.ts
│   │   │   └── schedulingService.ts
│   │   ├── types/                # TypeScript definitions
│   │   │   ├── workOrder.ts
│   │   │   ├── schedule.ts
│   │   │   └── machine.ts
│   │   ├── utils/                # Helper functions
│   │   │   ├── dateUtils.ts
│   │   │   └── schedulingUtils.ts
│   │   ├── hooks/                # Custom React hooks
│   │   │   ├── useWorkOrders.ts
│   │   │   └── useScheduling.ts
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   └── tsconfig.json
│
├── deployment/                    # Deployment configuration
│   ├── nginx.conf
│   ├── gunicorn.conf.py
│   ├── systemd/
│   │   └── mes-backend.service
│   └── docker-compose.yml        # Optional containerization
│
├── scripts/                       # Utility scripts
│   ├── migrate_data.py           # SQLite to PostgreSQL migration
│   ├── setup_dev.sh              # Development environment setup
│   └── deploy.sh                 # Deployment script
│
└── README.md
```

## Key Libraries

### Backend (Python)
```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1
pandas==2.1.3
pydantic==2.5.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

### Frontend (React)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "@dnd-kit/core": "^6.0.8",
    "@dnd-kit/sortable": "^8.0.0",
    "react-big-calendar": "^1.8.2",
    "date-fns": "^2.30.0",
    "axios": "^1.6.0",
    "react-router-dom": "^6.18.0",
    "react-query": "^3.39.3",
    "tailwindcss": "^3.3.0"
  }
}
```

## Development Phases (Accelerated Timeline)

### Phase 1: MVP Backend (1 week)
1. **FastAPI setup + PostgreSQL schema**
2. **Basic CRUD for work orders**
3. **Simple date-based sorting API**
4. **Data migration script**

### Phase 2: Core Scheduling (1 week)
1. **Basic scheduling algorithm (simplified VBA logic)**
2. **Date optimization (DatumIsporuke, DatumSastavljanja)**
3. **Status management (pending/finished)**
4. **Work center filtering**

### Phase 3: React Frontend (1 week)
1. **Basic React setup + work order list**
2. **Simple scheduling view (table/grid)**
3. **Date-based optimization controls**
4. **Mark as finished functionality**

### Phase 4: Drag-Drop + Polish (1 week)
1. **Drag-drop reordering**
2. **Real-time updates**
3. **Basic deployment to Ubuntu**
4. **Essential bug fixes**

**Total: 4 weeks for working MES system**

### Future Enhancements (Post-MVP)
- Advanced VBA algorithm porting
- Complex shift management
- Detailed reporting
- Performance optimization

## API Design Preview

### Work Orders
```python
# GET /api/work-orders
# POST /api/work-orders
# PUT /api/work-orders/{id}
# DELETE /api/work-orders/{id}
```

### Scheduling
```python
# POST /api/schedule/optimize
{
  "optimization_type": "datum_isporuke",  # or "datum_sastavljanja"
  "machine_id": "SAV100",
  "start_date": "2025-01-20",
  "work_order_ids": [1, 2, 3, 4]
}

# GET /api/schedule/{machine_id}
# PUT /api/schedule/reorder (for drag-drop)
```

### Machines
```python
# GET /api/machines
# GET /api/machines/{id}/calendar
# PUT /api/machines/{id}/status
```

## Next Steps
1. **Confirm technology stack approval**
2. **Set up development environment**
3. **Create PostgreSQL database schema**
4. **Start with Phase 1 implementation**

---
*Decision Date: January 2025*
*Stack: React + Python FastAPI + PostgreSQL*
*Target: Local Ubuntu server deployment*