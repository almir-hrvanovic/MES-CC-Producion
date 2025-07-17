"""
Work Center Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class WorkCenterBase(BaseModel):
    """Base work center schema"""
    plant_id: int = Field(..., description="Plant ID")
    code: str = Field(..., max_length=20, description="Work center code")
    name: str = Field(..., max_length=200, description="Work center name")
    description: Optional[str] = Field(None, description="Work center description")
    category_id: Optional[int] = Field(None, description="Work center category ID")
    capacity_hours_per_day: float = Field(default=8.0, description="Daily capacity in hours")
    setup_time_minutes: int = Field(default=0, description="Setup time in minutes")
    cost_per_hour: Optional[float] = Field(None, description="Cost per hour")
    is_active: bool = Field(default=True, description="Is work center active")


class WorkCenterCreate(WorkCenterBase):
    """Schema for creating work centers"""
    pass


class WorkCenterUpdate(BaseModel):
    """Schema for updating work centers"""
    plant_id: Optional[int] = Field(None, description="Plant ID")
    code: Optional[str] = Field(None, max_length=20, description="Work center code")
    name: Optional[str] = Field(None, max_length=200, description="Work center name")
    description: Optional[str] = Field(None, description="Work center description")
    category_id: Optional[int] = Field(None, description="Work center category ID")
    capacity_hours_per_day: Optional[float] = Field(None, description="Daily capacity in hours")
    setup_time_minutes: Optional[int] = Field(None, description="Setup time in minutes")
    cost_per_hour: Optional[float] = Field(None, description="Cost per hour")
    is_active: Optional[bool] = Field(None, description="Is work center active")


class WorkCenterResponse(WorkCenterBase):
    """Schema for work center responses"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class WorkCenterWithDetails(WorkCenterResponse):
    """Work center with category and plant information"""
    category: Optional[dict] = None
    plant: Optional[dict] = None
    
    class Config:
        from_attributes = True


class WorkCenterStatusUpdate(BaseModel):
    """Schema for updating work center status"""
    is_active: bool = Field(..., description="New active status")


class WorkCenterStatistics(BaseModel):
    """Schema for work center statistics"""
    operations_count: int
    status_distribution: dict[str, int]
    utilization_rate: float
    avg_setup_time: float
    current_operations: int
    
    class Config:
        from_attributes = True


class WorkCenterCapacityAnalysis(BaseModel):
    """Schema for work center capacity analysis"""
    total_time_needed_minutes: float
    daily_capacity_minutes: float
    total_capacity_minutes: float
    capacity_utilization_percent: float
    operations_count: int
    analysis_days: int
    average_operation_time: float
    
    class Config:
        from_attributes = True


class WorkCenterSchedule(BaseModel):
    """Schema for work center schedule"""
    date: Optional[str] = None
    operations: list[dict] = []
    total_operations: int
    total_time_minutes: float
    daily_capacity_minutes: float
    utilization_percent: float
    
    class Config:
        from_attributes = True


class WorkCenterPerformance(BaseModel):
    """Schema for work center performance metrics"""
    period_days: int
    completed_operations: int
    total_planned_time_minutes: float
    average_planned_time_minutes: float
    average_actual_time_minutes: float
    efficiency_percent: float
    operations_per_day: float
    
    class Config:
        from_attributes = True