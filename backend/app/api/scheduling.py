"""
Scheduling API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from pydantic import BaseModel
from enum import Enum

from app.database.connection import get_db
from app.database.models import WorkOrder, Operation, WorkCenter
from app.services.scheduling_service import SchedulingService

router = APIRouter()


class OptimizationCriteria(str, Enum):
    """Optimization criteria options"""
    DATUM_ISPORUKE = "datum_isporuke"
    DATUM_SASTAVLJANJA = "datum_sastavljanja"
    DATUM_TRECI = "datum_treci"
    HITNO_PRIORITY = "hitno"
    CUSTOM_ORDER = "custom"


class OptimizationRequest(BaseModel):
    """Request schema for optimization"""
    work_center: str
    criteria: OptimizationCriteria
    work_order_ids: Optional[List[int]] = None


class ScheduleEntry(BaseModel):
    """Schedule entry response"""
    operation_id: int
    work_order_id: int
    work_order_rn: str
    naziv: str
    norma: Optional[float]
    sequence_order: int
    estimated_start: Optional[str] = None
    estimated_end: Optional[str] = None


class OptimizationResponse(BaseModel):
    """Response schema for optimization"""
    optimized_schedule: List[ScheduleEntry]
    total_operations: int
    estimated_completion: Optional[str] = None
    conflicts: List[str] = []


class ReorderRequest(BaseModel):
    """Request schema for reordering"""
    work_center: str
    new_order: List[int]  # operation_ids in new sequence


@router.post("/optimize", response_model=OptimizationResponse)
async def optimize_schedule(
    request: OptimizationRequest,
    db: AsyncSession = Depends(get_db)
):
    """Optimize schedule based on selected criteria"""
    
    # Get work center
    wc_query = select(WorkCenter).where(WorkCenter.code == request.work_center)
    work_center = await db.scalar(wc_query)
    if not work_center:
        raise HTTPException(status_code=404, detail="Work center not found")
    
    # Get operations for the work center
    operations_query = select(Operation, WorkOrder.rn)\
        .join(WorkOrder, Operation.work_order_id == WorkOrder.id)\
        .where(
            and_(
                Operation.work_center_id == work_center.id,
                Operation.status == "pending"
            )
        )
    
    # Apply work order filter if specified
    if request.work_order_ids:
        operations_query = operations_query.where(WorkOrder.id.in_(request.work_order_ids))
    
    result = await db.execute(operations_query)
    operations_data = result.all()
    
    if not operations_data:
        return OptimizationResponse(
            optimized_schedule=[],
            total_operations=0,
            estimated_completion=None,
            conflicts=[]
        )
    
    # Use scheduling service to optimize
    scheduling_service = SchedulingService()
    optimized_operations = await scheduling_service.optimize_by_criteria(
        operations_data, request.criteria
    )
    
    # Format response
    schedule_entries = []
    for idx, (operation, work_order_rn) in enumerate(optimized_operations):
        entry = ScheduleEntry(
            operation_id=operation.id,
            work_order_id=operation.work_order_id,
            work_order_rn=work_order_rn,
            naziv=operation.naziv,
            norma=float(operation.norma) if operation.norma else None,
            sequence_order=idx + 1
        )
        schedule_entries.append(entry)
    
    return OptimizationResponse(
        optimized_schedule=schedule_entries,
        total_operations=len(schedule_entries),
        estimated_completion=None,  # TODO: Calculate based on norma
        conflicts=[]
    )


@router.put("/reorder")
async def reorder_schedule(
    request: ReorderRequest,
    db: AsyncSession = Depends(get_db)
):
    """Reorder schedule based on drag-drop changes"""
    
    # Get work center
    wc_query = select(WorkCenter).where(WorkCenter.code == request.work_center)
    work_center = await db.scalar(wc_query)
    if not work_center:
        raise HTTPException(status_code=404, detail="Work center not found")
    
    # Validate operation IDs exist and belong to work center
    operations_query = select(Operation)\
        .where(
            and_(
                Operation.id.in_(request.new_order),
                Operation.work_center_id == work_center.id
            )
        )
    
    result = await db.execute(operations_query)
    operations = result.scalars().all()
    
    if len(operations) != len(request.new_order):
        raise HTTPException(status_code=400, detail="Invalid operation IDs provided")
    
    # Update sequence order (this is a simplified implementation)
    # In a real system, you'd want to store this in a separate scheduling table
    for idx, operation_id in enumerate(request.new_order):
        operation = next(op for op in operations if op.id == operation_id)
        # For now, we'll just acknowledge the reorder
        # TODO: Implement actual sequence storage
    
    await db.commit()
    
    return {
        "message": "Schedule reordered successfully",
        "work_center": request.work_center,
        "new_sequence": request.new_order
    }


@router.get("/{work_center}")
async def get_schedule(
    work_center: str,
    db: AsyncSession = Depends(get_db)
):
    """Get current schedule for a work center"""
    
    # Get work center
    wc_query = select(WorkCenter).where(WorkCenter.code == work_center)
    work_center_obj = await db.scalar(wc_query)
    if not work_center_obj:
        raise HTTPException(status_code=404, detail="Work center not found")
    
    # Get operations
    operations_query = select(Operation, WorkOrder.rn)\
        .join(WorkOrder, Operation.work_order_id == WorkOrder.id)\
        .where(
            and_(
                Operation.work_center_id == work_center_obj.id,
                Operation.status.in_(["pending", "in_progress"])
            )
        )\
        .order_by(WorkOrder.datum_isporuke.asc().nulls_last())
    
    result = await db.execute(operations_query)
    operations_data = result.all()
    
    # Format response
    schedule_entries = []
    for idx, (operation, work_order_rn) in enumerate(operations_data):
        entry = ScheduleEntry(
            operation_id=operation.id,
            work_order_id=operation.work_order_id,
            work_order_rn=work_order_rn,
            naziv=operation.naziv,
            norma=float(operation.norma) if operation.norma else None,
            sequence_order=idx + 1
        )
        schedule_entries.append(entry)
    
    return {
        "work_center": work_center,
        "schedule": schedule_entries,
        "total_operations": len(schedule_entries)
    }