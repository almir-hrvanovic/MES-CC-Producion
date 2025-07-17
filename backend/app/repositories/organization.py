"""
Organization repository for multi-tenant management
"""
from typing import List, Optional, Dict, Any
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Organization, Plant, WorkCenter
from app.schemas.organization import OrganizationCreate, OrganizationUpdate
from .base import BaseRepository


class OrganizationRepository(BaseRepository[Organization, OrganizationCreate, OrganizationUpdate]):
    """
    Organization repository with multi-tenant management methods
    """
    
    def __init__(self, session: AsyncSession):
        super().__init__(Organization, session)
    
    async def get_by_code(self, code: str) -> Optional[Organization]:
        """Get organization by code"""
        stmt = select(Organization).where(Organization.code == code)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_with_plants(self, id: int) -> Optional[Organization]:
        """Get organization with all plants"""
        stmt = select(Organization).options(
            selectinload(Organization.plants)
        ).where(Organization.id == id)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_with_full_hierarchy(self, id: int) -> Optional[Organization]:
        """Get organization with complete hierarchy"""
        stmt = select(Organization).options(
            selectinload(Organization.plants).selectinload(Plant.work_centers)
        ).where(Organization.id == id)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_organization_statistics(self, id: int) -> Dict[str, Any]:
        """Get comprehensive organization statistics"""
        organization = await self.get_by_id(id)
        if not organization:
            return {"error": "Organization not found"}
        
        # Total plants
        plants_stmt = select(func.count(Plant.id)).where(
            Plant.organization_id == id
        )
        plants_result = await self.session.execute(plants_stmt)
        total_plants = plants_result.scalar()
        
        # Active plants
        active_plants_stmt = select(func.count(Plant.id)).where(
            and_(
                Plant.organization_id == id,
                Plant.is_active == True
            )
        )
        active_plants_result = await self.session.execute(active_plants_stmt)
        active_plants = active_plants_result.scalar()
        
        # Total work centers
        work_centers_stmt = select(func.count(WorkCenter.id)).join(Plant).where(
            Plant.organization_id == id
        )
        work_centers_result = await self.session.execute(work_centers_stmt)
        total_work_centers = work_centers_result.scalar()
        
        # Active work centers
        active_work_centers_stmt = select(func.count(WorkCenter.id)).join(Plant).where(
            and_(
                Plant.organization_id == id,
                WorkCenter.is_active == True
            )
        )
        active_work_centers_result = await self.session.execute(active_work_centers_stmt)
        active_work_centers = active_work_centers_result.scalar()
        
        return {
            "organization": organization,
            "statistics": {
                "total_plants": total_plants,
                "active_plants": active_plants,
                "total_work_centers": total_work_centers,
                "active_work_centers": active_work_centers
            }
        }
    
    async def search_organizations(
        self, 
        search_term: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Organization]:
        """Search organizations by code or name"""
        stmt = select(Organization).where(
            or_(
                Organization.code.ilike(f"%{search_term}%"),
                Organization.name.ilike(f"%{search_term}%")
            )
        ).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()