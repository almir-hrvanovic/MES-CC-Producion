"""
Operation repository for scheduling and production operations
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from sqlalchemy import select, func, and_, or_, update
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Operation, WorkOrder, WorkCenter, Product
from app.schemas.operation import OperationCreate, OperationUpdate
from .base import BaseRepository


class OperationRepository(BaseRepository[Operation, OperationCreate, OperationUpdate]):
    """
    Operation repository with scheduling-specific query methods
    """
    
    def __init__(self, session: AsyncSession):
        super().__init__(Operation, session)
    
    async def get_with_work_order(self, id: int) -> Optional[Operation]:
        """Get operation with work order information"""
        stmt = select(Operation).options(
            joinedload(Operation.work_order).joinedload(WorkOrder.product),
            joinedload(Operation.work_center)
        ).where(Operation.id == id)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_work_center(
        self, 
        work_center_code: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Operation]:
        """Get operations by work center"""
        stmt = select(Operation).options(
            joinedload(Operation.work_order).joinedload(WorkOrder.product),
            joinedload(Operation.work_center)
        ).join(WorkCenter).where(
            WorkCenter.code == work_center_code
        ).order_by(Operation.operation_sequence).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_work_order(self, work_order_id: int) -> List[Operation]:
        """Get all operations for a work order"""
        stmt = select(Operation).options(
            joinedload(Operation.work_center)
        ).where(Operation.work_order_id == work_order_id).order_by(
            Operation.operation_sequence
        )
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_status(
        self, 
        status: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Operation]:
        """Get operations by status"""
        stmt = select(Operation).options(
            joinedload(Operation.work_order).joinedload(WorkOrder.product),
            joinedload(Operation.work_center)
        ).where(Operation.status == status).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_scheduled_operations(
        self, 
        work_center_code: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Operation]:
        """Get scheduled operations for a work center with date filtering"""
        stmt = select(Operation).options(
            joinedload(Operation.work_order).joinedload(WorkOrder.product),
            joinedload(Operation.work_center)
        ).join(WorkCenter).where(WorkCenter.code == work_center_code)
        
        conditions = []
        
        if start_date:
            conditions.append(
                func.date(Operation.estimated_start_time) >= start_date
            )
        
        if end_date:
            conditions.append(
                func.date(Operation.estimated_completion_time) <= end_date
            )
        
        if conditions:
            stmt = stmt.where(and_(*conditions))
        
        stmt = stmt.order_by(
            Operation.estimated_start_time,
            Operation.operation_sequence
        )
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_operations_for_scheduling(
        self, 
        work_center_code: str
    ) -> Dict[str, Any]:
        """Get operations formatted for scheduling interface"""
        stmt = select(Operation).options(
            joinedload(Operation.work_order).joinedload(WorkOrder.product),
            joinedload(Operation.work_center)
        ).join(WorkCenter).where(
            and_(
                WorkCenter.code == work_center_code,
                Operation.status.in_(['pending', 'in_progress'])
            )
        ).order_by(Operation.operation_sequence)
        
        result = await self.session.execute(stmt)
        operations = result.scalars().all()
        
        # Get work center information
        work_center_stmt = select(WorkCenter).where(WorkCenter.code == work_center_code)
        work_center_result = await self.session.execute(work_center_stmt)
        work_center = work_center_result.scalar_one_or_none()
        
        return {
            "operations": operations,
            "work_center": work_center,
            "total_count": len(operations)
        }
    
    async def update_operation_sequence(
        self, 
        work_center_code: str, 
        operation_ids: List[int]
    ) -> bool:
        """Update operation sequence for scheduling"""
        try:
            # Update the sequence for each operation
            for index, operation_id in enumerate(operation_ids):
                stmt = update(Operation).where(
                    Operation.id == operation_id
                ).values(
                    operation_sequence=index + 1,
                    updated_at=datetime.utcnow()
                )
                await self.session.execute(stmt)
            
            await self.session.flush()
            return True
            
        except Exception as e:
            print(f"Error updating operation sequence: {e}")
            return False
    
    async def get_operation_statistics(
        self, 
        work_center_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get operation statistics for dashboard"""
        base_stmt = select(Operation)
        
        if work_center_code:
            base_stmt = base_stmt.join(WorkCenter).where(
                WorkCenter.code == work_center_code
            )
        
        # Total operations
        total_stmt = select(func.count(Operation.id))
        if work_center_code:
            total_stmt = total_stmt.join(WorkCenter).where(
                WorkCenter.code == work_center_code
            )
        
        total_result = await self.session.execute(total_stmt)
        total_operations = total_result.scalar()
        
        # Operations by status
        status_stmt = select(
            Operation.status,
            func.count(Operation.id).label('count')
        )
        if work_center_code:
            status_stmt = status_stmt.join(WorkCenter).where(
                WorkCenter.code == work_center_code
            )
        
        status_stmt = status_stmt.group_by(Operation.status)
        status_result = await self.session.execute(status_stmt)
        status_stats = {row.status: row.count for row in status_result.fetchall()}
        
        # Average operation time
        avg_time_stmt = select(func.avg(Operation.norma))
        if work_center_code:
            avg_time_stmt = avg_time_stmt.join(WorkCenter).where(
                WorkCenter.code == work_center_code
            )
        
        avg_time_result = await self.session.execute(avg_time_stmt)
        avg_time = avg_time_result.scalar() or 0
        
        return {
            "total_operations": total_operations,
            "status_distribution": status_stats,
            "average_operation_time": float(avg_time),
            "work_center": work_center_code
        }
    
    async def get_operations_by_priority(
        self, 
        work_center_code: str,
        limit: int = 100
    ) -> List[Operation]:
        """Get operations ordered by work order priority"""
        stmt = select(Operation).options(
            joinedload(Operation.work_order).joinedload(WorkOrder.product),
            joinedload(Operation.work_center)
        ).join(WorkOrder).join(WorkCenter).where(
            WorkCenter.code == work_center_code
        ).order_by(
            WorkOrder.priority_level,
            WorkOrder.datum_isporuke,
            Operation.operation_sequence
        ).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_operations_by_delivery_date(
        self, 
        work_center_code: str,
        limit: int = 100
    ) -> List[Operation]:
        """Get operations ordered by delivery date"""
        stmt = select(Operation).options(
            joinedload(Operation.work_order).joinedload(WorkOrder.product),
            joinedload(Operation.work_center)
        ).join(WorkOrder).join(WorkCenter).where(
            WorkCenter.code == work_center_code
        ).order_by(
            WorkOrder.datum_isporuke,
            Operation.operation_sequence
        ).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_operations_by_assembly_date(
        self, 
        work_center_code: str,
        limit: int = 100
    ) -> List[Operation]:
        """Get operations ordered by assembly date"""
        stmt = select(Operation).options(
            joinedload(Operation.work_order).joinedload(WorkOrder.product),
            joinedload(Operation.work_center)
        ).join(WorkOrder).join(WorkCenter).where(
            WorkCenter.code == work_center_code
        ).order_by(
            WorkOrder.datum_sastavljanja,
            Operation.operation_sequence
        ).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def update_operation_status(
        self, 
        id: int, 
        status: str,
        actual_start_time: Optional[datetime] = None,
        actual_completion_time: Optional[datetime] = None
    ) -> Optional[Operation]:
        """Update operation status and timestamps"""
        operation = await self.get_by_id(id)
        if not operation:
            return None
        
        operation.status = status
        operation.updated_at = datetime.utcnow()
        
        if actual_start_time:
            operation.actual_start_time = actual_start_time
        
        if actual_completion_time:
            operation.actual_completion_time = actual_completion_time
        
        await self.session.flush()
        await self.session.refresh(operation)
        return operation
    
    async def get_work_center_capacity(
        self, 
        work_center_code: str,
        date_filter: Optional[date] = None
    ) -> Dict[str, Any]:
        """Get work center capacity utilization"""
        
        # Get work center info
        work_center_stmt = select(WorkCenter).where(WorkCenter.code == work_center_code)
        work_center_result = await self.session.execute(work_center_stmt)
        work_center = work_center_result.scalar_one_or_none()
        
        if not work_center:
            return {"error": "Work center not found"}
        
        # Get operations for the date
        operations_stmt = select(Operation).join(WorkCenter).where(
            WorkCenter.code == work_center_code
        )
        
        if date_filter:
            operations_stmt = operations_stmt.where(
                func.date(Operation.estimated_start_time) == date_filter
            )
        
        operations_result = await self.session.execute(operations_stmt)
        operations = operations_result.scalars().all()
        
        # Calculate total time needed
        total_time = sum(op.norma or 0 for op in operations)
        
        # Calculate utilization
        daily_capacity = work_center.capacity_hours_per_day * 60  # Convert to minutes
        utilization_rate = (total_time / daily_capacity) * 100 if daily_capacity > 0 else 0
        
        return {
            "work_center": work_center,
            "operations_count": len(operations),
            "total_time_minutes": total_time,
            "daily_capacity_minutes": daily_capacity,
            "utilization_rate": min(utilization_rate, 100),  # Cap at 100%
            "date": date_filter
        }