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

## Development Timeline
- **Week 1**: MVP Backend (FastAPI + PostgreSQL)
- **Week 2**: Core Scheduling Logic
- **Week 3**: React Frontend
- **Week 4**: Drag-Drop + Deployment

## Quick Start
```bash
# Backend setup
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend setup
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