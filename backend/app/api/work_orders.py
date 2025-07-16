"""
Work Orders API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.database.connection import get_db
from app.database.models import WorkOrder, Product, Operation
from app.schemas.work_order import (
    WorkOrderCreate, 
    WorkOrderUpdate, 
    WorkOrderResponse, 
    WorkOrderWithProduct,
    WorkOrderListResponse
)

router = APIRouter()


@router.get("/", response_model=WorkOrderListResponse)
async def get_work_orders(
    work_center: Optional[str] = Query(None, description="Filter by work center code"),
    status: Optional[str] = Query(None, description="Filter by status"),
    urgent_only: bool = Query(False, description="Show only urgent orders (priority > 0)"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: AsyncSession = Depends(get_db)
):
    """Get list of work orders with filtering options"""
    
    # Build query
    query = select(WorkOrder, Product.name.label("product_name"), Product.kpl.label("product_kpl"))\
        .join(Product, WorkOrder.product_id == Product.id)
    
    # Apply filters
    if work_center:
        # Filter by work center through operations
        query = query.join(Operation, WorkOrder.id == Operation.work_order_id)\
            .join(WorkCenter, Operation.work_center_id == WorkCenter.id)\
            .where(WorkCenter.code == work_center)
    
    if status:
        query = query.where(WorkOrder.status == status)
    
    if urgent_only:
        query = query.where(WorkOrder.priority_level > 0)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_count = await db.scalar(count_query)
    
    # Apply pagination and execute
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    rows = result.all()
    
    # Format response
    work_orders = []
    for row in rows:
        work_order = WorkOrderWithProduct(
            id=row.WorkOrder.id,
            rn=row.WorkOrder.rn,
            product_id=row.WorkOrder.product_id,
            quantity=row.WorkOrder.quantity,
            priority_level=row.WorkOrder.priority_level,
            datum_isporuke=row.WorkOrder.datum_isporuke,
            datum_sastavljanja=row.WorkOrder.datum_sastavljanja,
            datum_treci=row.WorkOrder.datum_treci,
            status=row.WorkOrder.status,
            created_at=row.WorkOrder.created_at,
            updated_at=row.WorkOrder.updated_at,
            product_name=row.product_name,
            product_kpl=row.product_kpl
        )
        work_orders.append(work_order)
    
    # Get work center stats (placeholder)
    work_center_stats = {"SAV100": 0, "G1000": 0}  # TODO: Implement actual stats
    
    return WorkOrderListResponse(
        work_orders=work_orders,
        total_count=total_count or 0,
        work_center_stats=work_center_stats
    )


@router.post("/", response_model=WorkOrderResponse)
async def create_work_order(
    work_order: WorkOrderCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new work order"""
    
    # Check if product exists
    product_query = select(Product).where(Product.id == work_order.product_id)
    product = await db.scalar(product_query)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if RN already exists
    existing_query = select(WorkOrder).where(WorkOrder.rn == work_order.rn)
    existing = await db.scalar(existing_query)
    if existing:
        raise HTTPException(status_code=400, detail="Work order RN already exists")
    
    # Create work order
    db_work_order = WorkOrder(**work_order.model_dump())
    db.add(db_work_order)
    await db.commit()
    await db.refresh(db_work_order)
    
    return WorkOrderResponse.model_validate(db_work_order)


@router.get("/{work_order_id}", response_model=WorkOrderResponse)
async def get_work_order(
    work_order_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific work order by ID"""
    
    query = select(WorkOrder).where(WorkOrder.id == work_order_id)
    work_order = await db.scalar(query)
    
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    return WorkOrderResponse.model_validate(work_order)


@router.patch("/{work_order_id}/status")
async def update_work_order_status(
    work_order_id: int,
    status_update: dict,
    db: AsyncSession = Depends(get_db)
):
    """Update work order status"""
    
    query = select(WorkOrder).where(WorkOrder.id == work_order_id)
    work_order = await db.scalar(query)
    
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    # Update status
    if "status" in status_update:
        work_order.status = status_update["status"]
    
    await db.commit()
    await db.refresh(work_order)
    
    return {"message": "Status updated successfully", "work_order_id": work_order_id}


@router.put("/{work_order_id}", response_model=WorkOrderResponse)
async def update_work_order(
    work_order_id: int,
    work_order_update: WorkOrderUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a work order"""
    
    query = select(WorkOrder).where(WorkOrder.id == work_order_id)
    work_order = await db.scalar(query)
    
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    # Update fields
    update_data = work_order_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(work_order, field, value)
    
    await db.commit()
    await db.refresh(work_order)
    
    return WorkOrderResponse.model_validate(work_order)