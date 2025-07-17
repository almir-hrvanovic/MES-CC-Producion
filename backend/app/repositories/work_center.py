"""
Work Center repository for machine and resource management
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import WorkCenter, WorkCenterCategory, Plant, Operation
from app.schemas.work_center import WorkCenterCreate, WorkCenterUpdate
from .base import BaseRepository


class WorkCenterRepository(BaseRepository[WorkCenter, WorkCenterCreate, WorkCenterUpdate]):
    """
    Work Center repository with machine management methods
    """
    
    def __init__(self, session: AsyncSession):
        super().__init__(WorkCenter, session)
    
    async def get_with_category(self, id: int) -> Optional[WorkCenter]:
        """Get work center with category information"""
        stmt = select(WorkCenter).options(
            joinedload(WorkCenter.category),
            joinedload(WorkCenter.plant)
        ).where(WorkCenter.id == id)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_code(self, code: str) -> Optional[WorkCenter]:
        """Get work center by code"""
        stmt = select(WorkCenter).options(
            joinedload(WorkCenter.category),
            joinedload(WorkCenter.plant)
        ).where(WorkCenter.code == code)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_active_work_centers(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[WorkCenter]:
        """Get all active work centers"""
        stmt = select(WorkCenter).options(
            joinedload(WorkCenter.category),
            joinedload(WorkCenter.plant)
        ).where(WorkCenter.is_active == True).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_category(
        self, 
        category_code: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[WorkCenter]:
        """Get work centers by category"""
        stmt = select(WorkCenter).options(
            joinedload(WorkCenter.category),
            joinedload(WorkCenter.plant)
        ).join(WorkCenterCategory).where(
            WorkCenterCategory.category_code == category_code
        ).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_plant(
        self, 
        plant_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[WorkCenter]:
        """Get work centers by plant"""
        stmt = select(WorkCenter).options(
            joinedload(WorkCenter.category),
            joinedload(WorkCenter.plant)
        ).where(WorkCenter.plant_id == plant_id).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_work_centers_with_operations(self) -> List[WorkCenter]:
        """Get work centers with their current operations"""
        stmt = select(WorkCenter).options(
            joinedload(WorkCenter.category),
            joinedload(WorkCenter.plant),
            selectinload(WorkCenter.operations)
        ).where(WorkCenter.is_active == True)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_work_center_statistics(self, code: str) -> Dict[str, Any]:
        """Get comprehensive work center statistics"""
        work_center = await self.get_by_code(code)
        if not work_center:
            return {"error": "Work center not found"}
        
        # Total operations
        total_ops_stmt = select(func.count(Operation.id)).where(
            Operation.work_center_id == work_center.id
        )
        total_ops_result = await self.session.execute(total_ops_stmt)
        total_operations = total_ops_result.scalar()
        
        # Operations by status
        status_stmt = select(
            Operation.status,
            func.count(Operation.id).label('count')
        ).where(
            Operation.work_center_id == work_center.id
        ).group_by(Operation.status)
        
        status_result = await self.session.execute(status_stmt)
        status_distribution = {row.status: row.count for row in status_result.fetchall()}
        
        # Average setup time
        avg_setup_stmt = select(func.avg(Operation.norma)).where(
            Operation.work_center_id == work_center.id
        )
        avg_setup_result = await self.session.execute(avg_setup_stmt)
        avg_setup_time = avg_setup_result.scalar() or 0
        
        # Current utilization (operations in progress)
        current_ops_stmt = select(func.count(Operation.id)).where(
            and_(
                Operation.work_center_id == work_center.id,
                Operation.status == 'in_progress'
            )
        )
        current_ops_result = await self.session.execute(current_ops_stmt)
        current_operations = current_ops_result.scalar()
        
        # Calculate utilization rate
        utilization_rate = 0
        if total_operations > 0:
            utilization_rate = (current_operations / total_operations) * 100
        
        return {
            "work_center": work_center,
            "statistics": {
                "operations_count": total_operations,
                "status_distribution": status_distribution,
                "utilization_rate": utilization_rate,
                "avg_setup_time": float(avg_setup_time),
                "current_operations": current_operations
            }
        }
    
    async def get_work_center_capacity_analysis(
        self, 
        code: str,
        date_range: Optional[tuple] = None
    ) -> Dict[str, Any]:
        """Get detailed capacity analysis for work center"""
        work_center = await self.get_by_code(code)
        if not work_center:
            return {"error": "Work center not found"}
        
        # Base query for operations
        ops_stmt = select(Operation).where(Operation.work_center_id == work_center.id)
        
        if date_range:
            start_date, end_date = date_range
            ops_stmt = ops_stmt.where(
                and_(
                    func.date(Operation.estimated_start_time) >= start_date,
                    func.date(Operation.estimated_start_time) <= end_date
                )
            )
        
        ops_result = await self.session.execute(ops_stmt)
        operations = ops_result.scalars().all()
        
        # Calculate capacity metrics
        total_time_needed = sum(op.norma or 0 for op in operations)
        daily_capacity = work_center.capacity_hours_per_day * 60  # Convert to minutes
        
        # Days in analysis period
        if date_range:
            days = (date_range[1] - date_range[0]).days + 1
        else:
            days = 1
        
        total_capacity = daily_capacity * days
        capacity_utilization = (total_time_needed / total_capacity) * 100 if total_capacity > 0 else 0
        
        return {
            "work_center": work_center,
            "capacity_analysis": {
                "total_time_needed_minutes": total_time_needed,
                "daily_capacity_minutes": daily_capacity,
                "total_capacity_minutes": total_capacity,
                "capacity_utilization_percent": min(capacity_utilization, 100),
                "operations_count": len(operations),
                "analysis_days": days,
                "average_operation_time": total_time_needed / len(operations) if operations else 0
            }
        }
    
    async def get_work_center_schedule(
        self, 
        code: str,
        date_filter: Optional[date] = None
    ) -> Dict[str, Any]:
        """Get work center schedule for specific date"""
        work_center = await self.get_by_code(code)
        if not work_center:
            return {"error": "Work center not found"}
        
        # Get operations for the date
        ops_stmt = select(Operation).options(
            joinedload(Operation.work_order).joinedload(Operation.work_order.product)
        ).where(Operation.work_center_id == work_center.id)
        
        if date_filter:
            ops_stmt = ops_stmt.where(
                func.date(Operation.estimated_start_time) == date_filter
            )
        
        ops_stmt = ops_stmt.order_by(
            Operation.estimated_start_time,
            Operation.operation_sequence
        )
        
        ops_result = await self.session.execute(ops_stmt)
        operations = ops_result.scalars().all()
        
        # Calculate schedule metrics
        total_time = sum(op.norma or 0 for op in operations)
        daily_capacity = work_center.capacity_hours_per_day * 60
        
        return {
            "work_center": work_center,
            "schedule": {
                "date": date_filter,
                "operations": operations,
                "total_operations": len(operations),
                "total_time_minutes": total_time,
                "daily_capacity_minutes": daily_capacity,
                "utilization_percent": (total_time / daily_capacity) * 100 if daily_capacity > 0 else 0
            }
        }
    
    async def update_work_center_status(
        self, 
        code: str, 
        is_active: bool
    ) -> Optional[WorkCenter]:
        """Update work center active status"""
        work_center = await self.get_by_code(code)
        if not work_center:
            return None
        
        work_center.is_active = is_active
        work_center.updated_at = datetime.utcnow()
        
        await self.session.flush()
        await self.session.refresh(work_center)
        return work_center
    
    async def get_work_center_performance(
        self, 
        code: str,
        days_back: int = 30
    ) -> Dict[str, Any]:
        """Get work center performance metrics"""
        work_center = await self.get_by_code(code)
        if not work_center:
            return {"error": "Work center not found"}
        
        # Date range for analysis
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        # Completed operations in period
        completed_stmt = select(Operation).where(
            and_(
                Operation.work_center_id == work_center.id,
                Operation.status == 'completed',
                func.date(Operation.actual_completion_time) >= start_date,
                func.date(Operation.actual_completion_time) <= end_date
            )
        )
        
        completed_result = await self.session.execute(completed_stmt)
        completed_operations = completed_result.scalars().all()
        
        # Calculate performance metrics
        total_completed = len(completed_operations)
        total_planned_time = sum(op.norma or 0 for op in completed_operations)
        
        # Calculate actual vs planned time (if data available)
        actual_times = []
        for op in completed_operations:
            if op.actual_start_time and op.actual_completion_time:
                actual_time = (op.actual_completion_time - op.actual_start_time).total_seconds() / 60
                actual_times.append(actual_time)
        
        avg_actual_time = sum(actual_times) / len(actual_times) if actual_times else 0
        avg_planned_time = total_planned_time / total_completed if total_completed > 0 else 0
        
        efficiency = (avg_planned_time / avg_actual_time) * 100 if avg_actual_time > 0 else 0
        
        return {
            "work_center": work_center,
            "performance": {
                "period_days": days_back,
                "completed_operations": total_completed,
                "total_planned_time_minutes": total_planned_time,
                "average_planned_time_minutes": avg_planned_time,
                "average_actual_time_minutes": avg_actual_time,
                "efficiency_percent": min(efficiency, 200),  # Cap at 200% for realistic values
                "operations_per_day": total_completed / days_back if days_back > 0 else 0
            }
        }
    
    async def search_work_centers(
        self, 
        search_term: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[WorkCenter]:
        """Search work centers by code or name"""
        stmt = select(WorkCenter).options(
            joinedload(WorkCenter.category),
            joinedload(WorkCenter.plant)
        ).where(
            or_(
                WorkCenter.code.ilike(f"%{search_term}%"),
                WorkCenter.name.ilike(f"%{search_term}%"),
                WorkCenter.description.ilike(f"%{search_term}%")
            )
        ).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()