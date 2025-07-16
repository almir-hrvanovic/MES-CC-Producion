# MES Production Scheduling System - Backend

FastAPI backend for the Manufacturing Execution System.

## Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Database Setup
```bash
# Create PostgreSQL database 'mes_production'
# Run migrations
alembic upgrade head
```

### 5. Run Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/                 # API route handlers
│   │   ├── work_orders.py   # Work order endpoints
│   │   ├── scheduling.py    # Scheduling endpoints
│   │   └── machines.py      # Work center endpoints
│   ├── database/            # Database configuration
│   │   ├── connection.py    # Database connection
│   │   └── models.py        # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   │   └── scheduling_service.py
│   ├── utils/               # Utility functions
│   └── main.py              # FastAPI application
├── alembic/                 # Database migrations
├── requirements.txt         # Python dependencies
└── .env.example            # Environment template
```

## Key Features

- **Work Order Management**: CRUD operations for work orders
- **Date-based Optimization**: Sort by delivery dates, assembly dates
- **Work Center Support**: SAV100 (Press) and G1000 (CNC) machines
- **Scheduling API**: Optimize and reorder operations
- **Database Migrations**: Alembic for schema management
- **Async Support**: Full async/await implementation

## Development

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Testing
```bash
pytest
```

### Code Quality
```bash
# Format code
black app/

# Lint code
flake8 app/
```