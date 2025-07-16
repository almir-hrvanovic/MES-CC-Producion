"""
Pydantic schemas for work orders
"""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class WorkOrderBase(BaseModel):
    """Base work order schema"""
    rn: str
    quantity: int
    priority_level: int = 0
    datum_isporuke: Optional[date] = None
    datum_sastavljanja: Optional[date] = None
    datum_treci: Optional[date] = None
    status: str = "pending"


class WorkOrderCreate(WorkOrderBase):
    """Schema for creating work orders"""
    product_id: int


class WorkOrderUpdate(BaseModel):
    """Schema for updating work orders"""
    quantity: Optional[int] = None
    priority_level: Optional[int] = None
    datum_isporuke: Optional[date] = None
    datum_sastavljanja: Optional[date] = None
    datum_treci: Optional[date] = None
    status: Optional[str] = None


class WorkOrderResponse(WorkOrderBase):
    """Schema for work order responses"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime


class WorkOrderWithProduct(WorkOrderResponse):
    """Work order with product information"""
    product_name: str
    product_kpl: str


class WorkOrderListResponse(BaseModel):
    """Response schema for work order lists"""
    work_orders: List[WorkOrderWithProduct]
    total_count: int
    work_center_stats: dict