"""
Organization Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class OrganizationBase(BaseModel):
    """Base organization schema"""
    code: str = Field(..., max_length=20, description="Organization code")
    name: str = Field(..., max_length=200, description="Organization name")


class OrganizationCreate(OrganizationBase):
    """Schema for creating organizations"""
    pass


class OrganizationUpdate(BaseModel):
    """Schema for updating organizations"""
    code: Optional[str] = Field(None, max_length=20, description="Organization code")
    name: Optional[str] = Field(None, max_length=200, description="Organization name")


class OrganizationResponse(OrganizationBase):
    """Schema for organization responses"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrganizationWithPlants(OrganizationResponse):
    """Organization with plants information"""
    plants: list[dict] = []
    
    class Config:
        from_attributes = True


class OrganizationStatistics(BaseModel):
    """Schema for organization statistics"""
    total_plants: int
    active_plants: int
    total_work_centers: int
    active_work_centers: int
    
    class Config:
        from_attributes = True