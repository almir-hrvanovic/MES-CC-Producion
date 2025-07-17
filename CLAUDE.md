# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
MES Production Scheduling System - A FastAPI-based manufacturing execution system for production planning and scheduling. This is a modern web-based transition from an Excel VBA-based scheduling system.

## Key Commands

### Development Server
```bash
cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Operations
```bash
# Create migration
cd backend && alembic revision --autogenerate -m "description"

# Apply migrations
cd backend && alembic upgrade head

# Check migration status
cd backend && alembic current
```

### Testing and Quality
```bash
cd backend && pytest                    # Run tests
cd backend && pytest -v               # Verbose test output
cd backend && pytest tests/test_api.py  # Run specific test file
```

### Environment Setup
```bash
cd backend && python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
```

## Architecture

### Database Schema
Enterprise-level PostgreSQL schema with hierarchical structure:
- **Organization** → **Plant** → **WorkCenter** → **WorkOrder** → **Operation**
- **Product** definitions with BOM relationships
- **ScheduledOperation** for optimized scheduling
- Async SQLAlchemy 2.0 with proper foreign key relationships

### API Structure
RESTful API with three main modules:

**Work Orders** (`/api/work-orders`):
- List/filter work orders with status, work center, urgent flags
- CRUD operations with status transitions
- Bulk operations support

**Scheduling** (`/api/schedule`):
- POST `/optimize` - Optimize by delivery date, assembly date, priority
- PUT `/reorder` - Handle drag-drop reordering
- GET `/{work_center}` - Current schedule view

**Machines** (`/api/machines`):
- Work center management and status
- Calendar and availability (planned)
- Performance statistics

### Service Layer
**SchedulingService** (`app/services/scheduling_service.py`):
- Optimization algorithms for date-based sorting
- Conflict detection and resolution
- Supports multiple optimization criteria: `datum_isporuke`, `datum_sastavljanja`, `priority`

## Data Context
- **4,706 manufacturing operations** across 2 work centers
- **599 unique products (KPL)** with complex BOMs
- **1,746 work orders (RN)** spanning Dec 2024 - Sep 2025
- **Work Centers**: SAV100 (Press Brake), G1000 (CNC Milling)

## Database Configuration
- **Network Server**: MacBook Ubuntu 22.04 at `192.168.1.25:5432`
- **Connection**: Async PostgreSQL with `postgresql+asyncpg://almir:numipipdeedee@192.168.1.25:5432/mes_production`
- **User**: `almir` with CREATEDB privileges
- **Models**: Located in `app/database/models.py` with comprehensive relationships
- **Migrations**: Alembic configured in `alembic/` directory
- **Environment**: Uses pydantic-settings for configuration management

## Network Infrastructure
- **Web Server**: Nginx at `http://192.168.1.25` (Ubuntu 22.04)
- **Database**: PostgreSQL at `192.168.1.25:5432` (remote access enabled)
- **Message Queue**: RabbitMQ at `192.168.1.25:5672` (AMQP protocol)
- **Graph Database**: Neo4j at `http://192.168.1.25:7474` (web interface)
- **Network**: 1 Gbps via TP-Link LS1005G Switch
- **Security**: UFW firewall with specific port access rules

## Development Workflow
1. Database changes: Create migration → Apply → Test
2. API changes: Update route → Update schema → Test endpoint
3. Service logic: Implement in service layer → Test business logic
4. Use FastAPI docs at `http://localhost:8000/docs` for API testing

## Key Files
- `app/main.py`: FastAPI application with CORS and lifespan management
- `app/database/models.py`: Complete database schema with relationships
- `app/services/scheduling_service.py`: Core scheduling algorithms
- `alembic/env.py`: Database migration configuration
- `.env.example`: Environment variables template

## Business Logic
- **Scheduling Optimization**: Supports delivery date, assembly date, and priority-based sorting
- **Work Center Management**: Two-work-center system with capacity planning
- **Status Tracking**: Work order lifecycle management
- **Legacy Integration**: Migration from Excel VBA system (analysis in `legacy-analysis/`)

## Common Patterns
- Async/await throughout for database operations
- Pydantic schemas for request/response validation
- Dependency injection for services
- Repository pattern for data access
- Proper error handling with FastAPI HTTPException

## MCP Server Integration
MCP (Model Context Protocol) servers are configured for enhanced development:
- **PostgreSQL**: Direct database queries and schema inspection
- **File System**: Enhanced file operations across the project
- **Web Search**: Real-time documentation and troubleshooting
- **Git**: Advanced repository operations and history analysis
- **Fetch**: HTTP/HTTPS content fetching and web scraping capabilities
- **Context7**: Context management and memory enhancement across sessions

Configuration file: `claude_desktop_config.json`
Setup guide: `MCP_SETUP.md`


## Development Notes
- Always use descriptive variable names
- Local network setup documented in `homenetwork.md`

## Project Build and Development

- Build this project using claude-code sdk