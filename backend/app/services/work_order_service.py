"""
Work Order service layer with business logic
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.work_order import WorkOrderRepository
from app.repositories.operation import OperationRepository
from app.repositories.product import ProductRepository
from app.schemas.work_order import WorkOrderCreate, WorkOrderUpdate, WorkOrderResponse


class WorkOrderService:
    """
    Work Order service with business logic
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.work_order_repo = WorkOrderRepository(session)
        self.operation_repo = OperationRepository(session)
        self.product_repo = ProductRepository(session)
    
    async def create_work_order(self, work_order_data: WorkOrderCreate) -> WorkOrderResponse:
        """Create a new work order with validation"""
        # Validate product exists
        product = await self.product_repo.get_by_id(work_order_data.product_id)
        if not product:
            raise ValueError("Product not found")
        
        if not product.is_active:
            raise ValueError("Cannot create work order for inactive product")
        
        # Create work order
        work_order = await self.work_order_repo.create(work_order_data)
        await self.session.commit()
        
        return WorkOrderResponse.from_orm(work_order)
    
    async def get_work_order(self, id: int) -> Optional[WorkOrderResponse]:
        """Get work order by ID"""
        work_order = await self.work_order_repo.get_with_product(id)
        if not work_order:
            return None
        
        return WorkOrderResponse.from_orm(work_order)
    
    async def update_work_order(
        self, 
        id: int, 
        update_data: WorkOrderUpdate
    ) -> Optional[WorkOrderResponse]:
        """Update work order with validation"""
        work_order = await self.work_order_repo.get_by_id(id)
        if not work_order:
            return None
        
        # Validate product if being updated
        if update_data.product_id:
            product = await self.product_repo.get_by_id(update_data.product_id)
            if not product or not product.is_active:
                raise ValueError("Invalid or inactive product")
        
        updated_work_order = await self.work_order_repo.update(id, update_data)
        await self.session.commit()
        
        return WorkOrderResponse.from_orm(updated_work_order)
    
    async def delete_work_order(self, id: int) -> bool:
        """Delete work order with validation"""
        work_order = await self.work_order_repo.get_by_id(id)
        if not work_order:
            return False
        
        # Check if work order has operations in progress
        operations = await self.operation_repo.get_by_work_order(id)
        in_progress_ops = [op for op in operations if op.status == 'in_progress']
        
        if in_progress_ops:
            raise ValueError("Cannot delete work order with operations in progress")
        
        # Delete operations first
        for operation in operations:
            await self.operation_repo.delete(operation.id)
        
        # Delete work order
        success = await self.work_order_repo.delete(id)
        await self.session.commit()
        
        return success
    
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
        return await self.work_order_repo.get_work_orders_with_filters(
            status=status,
            priority_level=priority_level,
            work_center=work_center,
            urgent_only=urgent_only,
            skip=skip,
            limit=limit
        )
    
    async def update_work_order_status(
        self, 
        id: int, 
        status: str
    ) -> Optional[WorkOrderResponse]:
        """Update work order status with business logic"""
        work_order = await self.work_order_repo.get_by_id(id)
        if not work_order:
            return None
        
        # Validate status transition
        valid_transitions = {
            'pending': ['in_progress', 'cancelled'],
            'in_progress': ['completed', 'cancelled'],
            'completed': [],
            'cancelled': ['pending']
        }
        
        if status not in valid_transitions.get(work_order.status, []):
            raise ValueError(f"Invalid status transition from {work_order.status} to {status}")
        
        # Update related operations if needed
        if status == 'completed':
            operations = await self.operation_repo.get_by_work_order(id)
            for operation in operations:
                if operation.status in ['pending', 'in_progress']:
                    await self.operation_repo.update_operation_status(
                        operation.id, 
                        'completed',
                        actual_completion_time=datetime.utcnow()
                    )
        
        updated_work_order = await self.work_order_repo.update_status(id, status)
        await self.session.commit()
        
        return WorkOrderResponse.from_orm(updated_work_order)
    
    async def get_dashboard_statistics(self) -> Dict[str, Any]:
        """Get dashboard statistics for work orders"""
        return await self.work_order_repo.get_dashboard_statistics()
    
    async def get_recent_work_orders(self, limit: int = 5) -> List[WorkOrderResponse]:
        """Get recently updated work orders"""
        work_orders = await self.work_order_repo.get_recent_work_orders(limit)
        return [WorkOrderResponse.from_orm(wo) for wo in work_orders]
    
    async def get_overdue_work_orders(self) -> List[WorkOrderResponse]:
        """Get overdue work orders"""
        work_orders = await self.work_order_repo.get_overdue_orders()
        return [WorkOrderResponse.from_orm(wo) for wo in work_orders]
    
    async def get_urgent_work_orders(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[WorkOrderResponse]:
        """Get urgent work orders"""
        work_orders = await self.work_order_repo.get_urgent_orders(skip, limit)
        return [WorkOrderResponse.from_orm(wo) for wo in work_orders]
    
    async def search_work_orders(
        self, 
        search_term: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[WorkOrderResponse]:
        """Search work orders"""
        work_orders = await self.work_order_repo.search_work_orders(search_term, skip, limit)
        return [WorkOrderResponse.from_orm(wo) for wo in work_orders]
    
    async def get_work_orders_by_date_range(
        self, 
        start_date: date, 
        end_date: date,
        skip: int = 0, 
        limit: int = 100
    ) -> List[WorkOrderResponse]:
        """Get work orders by delivery date range"""
        work_orders = await self.work_order_repo.get_by_delivery_date_range(
            start_date, end_date, skip, limit
        )
        return [WorkOrderResponse.from_orm(wo) for wo in work_orders]
    
    async def validate_work_order_data(self, data: WorkOrderCreate) -> List[str]:
        """Validate work order data and return list of errors"""
        errors = []
        
        # Validate product exists and is active
        product = await self.product_repo.get_by_id(data.product_id)
        if not product:
            errors.append("Product not found")
        elif not product.is_active:
            errors.append("Product is inactive")
        
        # Validate priority level
        if data.priority_level not in [1, 2, 3]:
            errors.append("Priority level must be 1, 2, or 3")
        
        # Validate quantity
        if data.quantity <= 0:
            errors.append("Quantity must be greater than 0")
        
        # Validate dates
        if data.datum_isporuke and data.datum_sastavljanja:
            if data.datum_isporuke < data.datum_sastavljanja:
                errors.append("Delivery date cannot be before assembly date")
        
        return errors