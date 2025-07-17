"""
Work Order repository for database operations
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import WorkOrder, Product, Operation, WorkCenter
from app.schemas.work_order import WorkOrderCreate, WorkOrderUpdate
from .base import BaseRepository


class WorkOrderRepository(BaseRepository[WorkOrder, WorkOrderCreate, WorkOrderUpdate]):
    """
    Work Order repository with specialized query methods
    """
    
    def __init__(self, session: AsyncSession):
        super().__init__(WorkOrder, session)
    
    async def get_with_product(self, id: int) -> Optional[WorkOrder]:
        """Get work order with product information"""
        stmt = select(WorkOrder).options(
            joinedload(WorkOrder.product)
        ).where(WorkOrder.id == id)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_with_operations(self, id: int) -> Optional[WorkOrder]:
        """Get work order with all operations"""
        stmt = select(WorkOrder).options(
            joinedload(WorkOrder.product),
            selectinload(WorkOrder.operations).joinedload(Operation.work_center)
        ).where(WorkOrder.id == id)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_status(
        self, 
        status: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[WorkOrder]:
        """Get work orders by status"""
        stmt = select(WorkOrder).options(
            joinedload(WorkOrder.product)
        ).where(WorkOrder.status == status).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_priority(
        self, 
        priority_level: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[WorkOrder]:
        """Get work orders by priority level"""
        stmt = select(WorkOrder).options(
            joinedload(WorkOrder.product)
        ).where(WorkOrder.priority_level == priority_level).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_delivery_date_range(
        self, 
        start_date: date, 
        end_date: date,
        skip: int = 0, 
        limit: int = 100
    ) -> List[WorkOrder]:
        """Get work orders by delivery date range"""
        stmt = select(WorkOrder).options(
            joinedload(WorkOrder.product)
        ).where(
            and_(
                WorkOrder.datum_isporuke >= start_date,
                WorkOrder.datum_isporuke <= end_date
            )
        ).order_by(WorkOrder.datum_isporuke).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_urgent_orders(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[WorkOrder]:
        """Get urgent work orders (priority level 1)"""
        stmt = select(WorkOrder).options(
            joinedload(WorkOrder.product)
        ).where(WorkOrder.priority_level == 1).order_by(
            WorkOrder.datum_isporuke
        ).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_overdue_orders(self, current_date: date = None) -> List[WorkOrder]:
        """Get overdue work orders"""
        if current_date is None:
            current_date = datetime.now().date()
        
        stmt = select(WorkOrder).options(
            joinedload(WorkOrder.product)
        ).where(
            and_(
                WorkOrder.datum_isporuke < current_date,
                WorkOrder.status.in_(['pending', 'in_progress'])
            )
        ).order_by(WorkOrder.datum_isporuke)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def search_work_orders(
        self, 
        search_term: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[WorkOrder]:
        """Search work orders by RN or product name"""
        stmt = select(WorkOrder).options(
            joinedload(WorkOrder.product)
        ).where(
            or_(
                WorkOrder.rn.ilike(f"%{search_term}%"),
                Product.name.ilike(f"%{search_term}%"),
                Product.kpl.ilike(f"%{search_term}%")
            )
        ).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_work_orders_with_filters(
        self,
        status: Optional[str] = None,
        priority_level: Optional[int] = None,
        work_center: Optional[str] = None,
        urgent_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get work orders with comprehensive filtering"""
        
        # Base query with product join
        stmt = select(WorkOrder).options(
            joinedload(WorkOrder.product)
        )
        
        # Apply filters
        conditions = []
        
        if status:
            conditions.append(WorkOrder.status == status)
        
        if priority_level:
            conditions.append(WorkOrder.priority_level == priority_level)
        
        if urgent_only:
            conditions.append(WorkOrder.priority_level == 1)
        
        if work_center:
            # Filter by work center through operations
            stmt = stmt.join(Operation).join(WorkCenter)
            conditions.append(WorkCenter.code == work_center)
        
        if conditions:
            stmt = stmt.where(and_(*conditions))
        
        # Get total count for pagination
        count_stmt = select(func.count(WorkOrder.id))
        if conditions:
            if work_center:
                count_stmt = count_stmt.join(Operation).join(WorkCenter)
            count_stmt = count_stmt.where(and_(*conditions))
        
        # Execute count query
        count_result = await self.session.execute(count_stmt)
        total_count = count_result.scalar()
        
        # Apply pagination and ordering
        stmt = stmt.order_by(
            WorkOrder.priority_level,
            WorkOrder.datum_isporuke
        ).offset(skip).limit(limit)
        
        # Execute main query
        result = await self.session.execute(stmt)
        work_orders = result.scalars().all()
        
        # Get work center statistics
        work_center_stats = await self.get_work_center_statistics()
        
        return {
            "work_orders": work_orders,
            "total_count": total_count,
            "work_center_stats": work_center_stats
        }
    
    async def get_work_center_statistics(self) -> Dict[str, int]:
        """Get work center distribution statistics"""
        stmt = select(
            WorkCenter.code,
            func.count(WorkOrder.id).label('count')
        ).join(Operation).join(WorkOrder).group_by(WorkCenter.code)
        
        result = await self.session.execute(stmt)
        return {row.code: row.count for row in result.fetchall()}
    
    async def update_status(self, id: int, status: str) -> Optional[WorkOrder]:
        """Update work order status"""
        work_order = await self.get_by_id(id)
        if not work_order:
            return None
        
        work_order.status = status
        work_order.updated_at = datetime.utcnow()
        
        await self.session.flush()
        await self.session.refresh(work_order)
        return work_order
    
    async def get_dashboard_statistics(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        # Active work orders
        active_stmt = select(func.count(WorkOrder.id)).where(
            WorkOrder.status == 'in_progress'
        )
        active_result = await self.session.execute(active_stmt)
        active_count = active_result.scalar()
        
        # Completed today
        today = datetime.now().date()
        completed_stmt = select(func.count(WorkOrder.id)).where(
            and_(
                WorkOrder.status == 'completed',
                func.date(WorkOrder.updated_at) == today
            )
        )
        completed_result = await self.session.execute(completed_stmt)
        completed_today = completed_result.scalar()
        
        # Pending work orders
        pending_stmt = select(func.count(WorkOrder.id)).where(
            WorkOrder.status == 'pending'
        )
        pending_result = await self.session.execute(pending_stmt)
        pending_count = pending_result.scalar()
        
        # Urgent work orders
        urgent_stmt = select(func.count(WorkOrder.id)).where(
            WorkOrder.priority_level == 1
        )
        urgent_result = await self.session.execute(urgent_stmt)
        urgent_count = urgent_result.scalar()
        
        return {
            "active_count": active_count,
            "completed_today": completed_today,
            "pending_count": pending_count,
            "urgent_count": urgent_count
        }
    
    async def get_recent_work_orders(self, limit: int = 5) -> List[WorkOrder]:
        """Get recently updated work orders"""
        stmt = select(WorkOrder).options(
            joinedload(WorkOrder.product)
        ).order_by(WorkOrder.updated_at.desc()).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()