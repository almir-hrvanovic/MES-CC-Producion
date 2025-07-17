"""
Product repository for product management
"""
from typing import List, Optional, Dict, Any
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Product, ProductType, WorkOrder
from app.schemas.product import ProductCreate, ProductUpdate
from .base import BaseRepository


class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    """
    Product repository with product management methods
    """
    
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)
    
    async def get_with_type(self, id: int) -> Optional[Product]:
        """Get product with type information"""
        stmt = select(Product).options(
            joinedload(Product.type)
        ).where(Product.id == id)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_kpl(self, kpl: str) -> Optional[Product]:
        """Get product by KPL code"""
        stmt = select(Product).options(
            joinedload(Product.type)
        ).where(Product.kpl == kpl)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_type(
        self, 
        type_code: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Product]:
        """Get products by type"""
        stmt = select(Product).options(
            joinedload(Product.type)
        ).join(ProductType).where(
            ProductType.type_code == type_code
        ).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_active_products(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Product]:
        """Get all active products"""
        stmt = select(Product).options(
            joinedload(Product.type)
        ).where(Product.is_active == True).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def search_products(
        self, 
        search_term: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Product]:
        """Search products by KPL, name, or description"""
        stmt = select(Product).options(
            joinedload(Product.type)
        ).where(
            or_(
                Product.kpl.ilike(f"%{search_term}%"),
                Product.name.ilike(f"%{search_term}%"),
                Product.description.ilike(f"%{search_term}%")
            )
        ).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_products_with_work_orders(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Product]:
        """Get products that have work orders"""
        stmt = select(Product).options(
            joinedload(Product.type),
            selectinload(Product.work_orders)
        ).join(WorkOrder).distinct().offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_product_statistics(self, id: int) -> Dict[str, Any]:
        """Get product statistics"""
        product = await self.get_with_type(id)
        if not product:
            return {"error": "Product not found"}
        
        # Total work orders
        total_wo_stmt = select(func.count(WorkOrder.id)).where(
            WorkOrder.product_id == id
        )
        total_wo_result = await self.session.execute(total_wo_stmt)
        total_work_orders = total_wo_result.scalar()
        
        # Work orders by status
        status_stmt = select(
            WorkOrder.status,
            func.count(WorkOrder.id).label('count')
        ).where(
            WorkOrder.product_id == id
        ).group_by(WorkOrder.status)
        
        status_result = await self.session.execute(status_stmt)
        status_distribution = {row.status: row.count for row in status_result.fetchall()}
        
        # Total quantity ordered
        quantity_stmt = select(func.sum(WorkOrder.quantity)).where(
            WorkOrder.product_id == id
        )
        quantity_result = await self.session.execute(quantity_stmt)
        total_quantity = quantity_result.scalar() or 0
        
        return {
            "product": product,
            "statistics": {
                "total_work_orders": total_work_orders,
                "status_distribution": status_distribution,
                "total_quantity_ordered": total_quantity
            }
        }
    
    async def get_products_by_priority(
        self, 
        priority_level: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Product]:
        """Get products by priority level"""
        stmt = select(Product).options(
            joinedload(Product.type)
        ).where(Product.priority_level == priority_level).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def update_product_status(
        self, 
        id: int, 
        is_active: bool
    ) -> Optional[Product]:
        """Update product active status"""
        product = await self.get_by_id(id)
        if not product:
            return None
        
        product.is_active = is_active
        
        await self.session.flush()
        await self.session.refresh(product)
        return product