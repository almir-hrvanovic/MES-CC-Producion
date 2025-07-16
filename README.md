# MES Production Scheduling System

Modern web-based Manufacturing Execution System (MES) for production planning and scheduling.

## Overview
Transition from Excel VBA-based scheduling system to modern web application with:
- Date-based optimization (delivery dates, assembly dates)
- Drag-drop schedule fine-tuning
- Real-time production status management
- Multi-work center support

## Technology Stack
- **Frontend**: React + TypeScript
- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **Deployment**: Ubuntu + Nginx

## Project Structure
```
mes-production-scheduler/
├── backend/                 # Python FastAPI backend
├── frontend/               # React TypeScript frontend
├── deployment/             # Deployment configurations
├── scripts/               # Utility scripts
├── legacy-analysis/       # Original VBA system analysis
└── docs/                  # Documentation
```

## Development Status

### ✅ Completed (Week 1 - Phase 1)
- **Project Structure**: Complete organization with clean separation
- **Database Design**: Enterprise-level PostgreSQL schema designed
- **FastAPI Backend**: Complete backend structure with API endpoints
- **Kiro Specs**: Requirements, design, and implementation tasks defined
- **Documentation**: Comprehensive project documentation

### 🔄 In Progress
- **Task 2**: PostgreSQL database schema and migration system

### ⏳ Upcoming
- **Tasks 3-4**: Data migration and core database operations
- **Tasks 5-8**: Core API development and business logic
- **Tasks 9-12**: React frontend development
- **Tasks 13-20**: Advanced features and deployment

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup (Coming Soon)
```bash
cd frontend
npm install
npm start
```

## Data Overview
- **4,706 manufacturing operations**
- **599 unique products (KPL)**
- **1,746 work orders (RN)**
- **2 work centers**: SAV100 (Press), G1000 (CNC)
- **Date range**: Dec 2024 - Sep 2025

## Legacy System
Original VBA-based system analysis and data extraction tools are located in `legacy-analysis/` folder.

---
*Project Status: Development Phase*
*Target: 4-week MVP delivery*