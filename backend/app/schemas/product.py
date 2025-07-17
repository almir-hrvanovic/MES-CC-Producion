"""
Product Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base product schema"""
    type_id: int = Field(..., description="Product type ID")
    kpl: str = Field(..., max_length=50, description="Product KPL code")
    name: str = Field(..., max_length=200, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    priority_level: int = Field(default=3, description="Product priority level")
    is_active: bool = Field(default=True, description="Is product active")


class ProductCreate(ProductBase):
    """Schema for creating products"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating products"""
    type_id: Optional[int] = Field(None, description="Product type ID")
    kpl: Optional[str] = Field(None, max_length=50, description="Product KPL code")
    name: Optional[str] = Field(None, max_length=200, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    priority_level: Optional[int] = Field(None, description="Product priority level")
    is_active: Optional[bool] = Field(None, description="Is product active")


class ProductResponse(ProductBase):
    """Schema for product responses"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductWithType(ProductResponse):
    """Product with type information"""
    type: Optional[dict] = None
    
    class Config:
        from_attributes = True


class ProductWithWorkOrders(ProductResponse):
    """Product with work orders information"""
    work_orders: list[dict] = []
    
    class Config:
        from_attributes = True


class ProductStatusUpdate(BaseModel):
    """Schema for updating product status"""
    is_active: bool = Field(..., description="New active status")


class ProductStatistics(BaseModel):
    """Schema for product statistics"""
    total_work_orders: int
    status_distribution: dict[str, int]
    total_quantity_ordered: int
    
    class Config:
        from_attributes = True