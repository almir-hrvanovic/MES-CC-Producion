"""
Machines/Work Centers API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel

from app.database.connection import get_db
from app.database.models import WorkCenter, WorkCenterCategory, Operation

router = APIRouter()


class WorkCenterResponse(BaseModel):
    """Work center response schema"""
    id: int
    code: str
    name: str
    description: Optional[str]
    capacity_hours_per_day: float
    setup_time_minutes: int
    cost_per_hour: Optional[float]
    is_active: bool
    
    class Config:
        from_attributes = True


class WorkCenterStats(BaseModel):
    """Work center statistics"""
    total_operations: int
    pending_operations: int
    in_progress_operations: int
    completed_operations: int
    total_hours: float


class WorkCenterWithStats(WorkCenterResponse):
    """Work center with statistics"""
    stats: WorkCenterStats


@router.get("/", response_model=List[WorkCenterResponse])
async def get_work_centers(
    active_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """Get list of work centers"""
    
    query = select(WorkCenter)
    if active_only:
        query = query.where(WorkCenter.is_active == True)
    
    query = query.order_by(WorkCenter.code)
    result = await db.execute(query)
    work_centers = result.scalars().all()
    
    return [WorkCenterResponse.model_validate(wc) for wc in work_centers]


@router.get("/{work_center_code}", response_model=WorkCenterWithStats)
async def get_work_center(
    work_center_code: str,
    db: AsyncSession = Depends(get_db)
):
    """Get specific work center with statistics"""
    
    # Get work center
    wc_query = select(WorkCenter).where(WorkCenter.code == work_center_code)
    work_center = await db.scalar(wc_query)
    
    if not work_center:
        raise HTTPException(status_code=404, detail="Work center not found")
    
    # Get statistics
    stats_query = select(
        func.count(Operation.id).label("total_operations"),
        func.count().filter(Operation.status == "pending").label("pending_operations"),
        func.count().filter(Operation.status == "in_progress").label("in_progress_operations"),
        func.count().filter(Operation.status == "completed").label("completed_operations"),
        func.coalesce(func.sum(Operation.norma), 0).label("total_hours")
    ).where(Operation.work_center_id == work_center.id)
    
    result = await db.execute(stats_query)
    stats_row = result.first()
    
    stats = WorkCenterStats(
        total_operations=stats_row.total_operations or 0,
        pending_operations=stats_row.pending_operations or 0,
        in_progress_operations=stats_row.in_progress_operations or 0,
        completed_operations=stats_row.completed_operations or 0,
        total_hours=float(stats_row.total_hours or 0)
    )
    
    return WorkCenterWithStats(
        **WorkCenterResponse.model_validate(work_center).model_dump(),
        stats=stats
    )


@router.get("/{work_center_code}/calendar")
async def get_work_center_calendar(
    work_center_code: str,
    db: AsyncSession = Depends(get_db)
):
    """Get work center calendar (placeholder for future implementation)"""
    
    # Get work center
    wc_query = select(WorkCenter).where(WorkCenter.code == work_center_code)
    work_center = await db.scalar(wc_query)
    
    if not work_center:
        raise HTTPException(status_code=404, detail="Work center not found")
    
    # Placeholder calendar data
    return {
        "work_center": work_center_code,
        "calendar": "Calendar functionality to be implemented",
        "shifts": {
            "shift_1": "07:00-15:00",
            "shift_2": "15:00-23:00", 
            "shift_3": "23:00-07:00"
        }
    }


@router.put("/{work_center_code}/status")
async def update_work_center_status(
    work_center_code: str,
    status_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """Update work center status"""
    
    # Get work center
    wc_query = select(WorkCenter).where(WorkCenter.code == work_center_code)
    work_center = await db.scalar(wc_query)
    
    if not work_center:
        raise HTTPException(status_code=404, detail="Work center not found")
    
    # Update status
    if "is_active" in status_data:
        work_center.is_active = status_data["is_active"]
    
    await db.commit()
    
    return {
        "message": "Work center status updated",
        "work_center": work_center_code,
        "is_active": work_center.is_active
    }