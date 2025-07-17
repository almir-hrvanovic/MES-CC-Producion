"""
Work Orders API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.services.work_order_service import WorkOrderService
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
    
    service = WorkOrderService(db)
    
    try:
        result = await service.get_work_orders_with_filters(
            status=status,
            work_center=work_center,
            urgent_only=urgent_only,
            skip=offset,
            limit=limit
        )
        
        # Format work orders for response
        work_orders = []
        for wo in result["work_orders"]:
            work_order = WorkOrderWithProduct(
                id=wo.id,
                rn=wo.rn,
                product_id=wo.product_id,
                quantity=wo.quantity,
                priority_level=wo.priority_level,
                datum_isporuke=wo.datum_isporuke,
                datum_sastavljanja=wo.datum_sastavljanja,
                datum_treci=wo.datum_treci,
                status=wo.status,
                created_at=wo.created_at,
                updated_at=wo.updated_at,
                product_name=wo.product.name if wo.product else "",
                product_kpl=wo.product.kpl if wo.product else ""
            )
            work_orders.append(work_order)
        
        return WorkOrderListResponse(
            work_orders=work_orders,
            total_count=result["total_count"],
            work_center_stats=result["work_center_stats"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=WorkOrderResponse)
async def create_work_order(
    work_order: WorkOrderCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new work order"""
    
    service = WorkOrderService(db)
    
    try:
        # Validate work order data
        validation_errors = await service.validate_work_order_data(work_order)
        if validation_errors:
            raise HTTPException(status_code=400, detail={"errors": validation_errors})
        
        # Create work order
        created_work_order = await service.create_work_order(work_order)
        return created_work_order
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{work_order_id}", response_model=WorkOrderResponse)
async def get_work_order(
    work_order_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific work order by ID"""
    
    service = WorkOrderService(db)
    
    work_order = await service.get_work_order(work_order_id)
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    return work_order


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