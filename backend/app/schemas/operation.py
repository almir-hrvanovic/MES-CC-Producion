"""
Operation Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class OperationBase(BaseModel):
    """Base operation schema"""
    work_order_id: int = Field(..., description="Work order ID")
    work_center_id: int = Field(..., description="Work center ID")
    operation_sequence: int = Field(..., description="Operation sequence number")
    naziv: str = Field(..., max_length=500, description="Operation name")
    norma: Optional[float] = Field(None, description="Standard time in minutes")
    quantity: int = Field(default=1, description="Quantity to produce")
    quantity_completed: int = Field(default=0, description="Quantity completed")
    status: str = Field(default="pending", description="Operation status")
    estimated_start_time: Optional[datetime] = Field(None, description="Estimated start time")
    estimated_completion_time: Optional[datetime] = Field(None, description="Estimated completion time")


class OperationCreate(OperationBase):
    """Schema for creating operations"""
    pass


class OperationUpdate(BaseModel):
    """Schema for updating operations"""
    work_center_id: Optional[int] = Field(None, description="Work center ID")
    operation_sequence: Optional[int] = Field(None, description="Operation sequence number")
    naziv: Optional[str] = Field(None, max_length=500, description="Operation name")
    norma: Optional[float] = Field(None, description="Standard time in minutes")
    quantity: Optional[int] = Field(None, description="Quantity to produce")
    quantity_completed: Optional[int] = Field(None, description="Quantity completed")
    status: Optional[str] = Field(None, description="Operation status")
    estimated_start_time: Optional[datetime] = Field(None, description="Estimated start time")
    estimated_completion_time: Optional[datetime] = Field(None, description="Estimated completion time")
    actual_start_time: Optional[datetime] = Field(None, description="Actual start time")
    actual_completion_time: Optional[datetime] = Field(None, description="Actual completion time")


class OperationResponse(OperationBase):
    """Schema for operation responses"""
    id: int
    actual_start_time: Optional[datetime] = None
    actual_completion_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OperationWithWorkOrder(OperationResponse):
    """Operation with work order information"""
    work_order: Optional[dict] = None
    work_center: Optional[dict] = None
    
    class Config:
        from_attributes = True


class OperationStatusUpdate(BaseModel):
    """Schema for updating operation status"""
    status: str = Field(..., description="New operation status")
    actual_start_time: Optional[datetime] = Field(None, description="Actual start time")
    actual_completion_time: Optional[datetime] = Field(None, description="Actual completion time")


class OperationSequenceUpdate(BaseModel):
    """Schema for updating operation sequence"""
    operation_ids: list[int] = Field(..., description="List of operation IDs in new order")


class OperationStatistics(BaseModel):
    """Schema for operation statistics"""
    total_operations: int
    status_distribution: dict[str, int]
    average_operation_time: float
    work_center: Optional[str] = None
    
    class Config:
        from_attributes = True