"""
Base repository class with common CRUD operations
"""
from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload

from app.database.connection import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository class with common CRUD operations
    """
    
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get a record by ID"""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None
    ) -> List[ModelType]:
        """Get all records with optional filtering and pagination"""
        stmt = select(self.model)
        
        # Apply filters
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    column = getattr(self.model, key)
                    if isinstance(value, list):
                        stmt = stmt.where(column.in_(value))
                    else:
                        stmt = stmt.where(column == value)
        
        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            stmt = stmt.order_by(getattr(self.model, order_by))
        
        # Apply pagination
        stmt = stmt.offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record"""
        if hasattr(obj_in, 'dict'):
            obj_data = obj_in.dict()
        else:
            obj_data = obj_in
        
        db_obj = self.model(**obj_data)
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj
    
    async def update(self, id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        """Update an existing record"""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None
        
        if hasattr(obj_in, 'dict'):
            obj_data = obj_in.dict(exclude_unset=True)
        else:
            obj_data = obj_in
        
        for field, value in obj_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj
    
    async def delete(self, id: int) -> bool:
        """Delete a record by ID"""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return False
        
        await self.session.delete(db_obj)
        await self.session.flush()
        return True
    
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records with optional filtering"""
        stmt = select(func.count(self.model.id))
        
        # Apply filters
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    column = getattr(self.model, key)
                    if isinstance(value, list):
                        stmt = stmt.where(column.in_(value))
                    else:
                        stmt = stmt.where(column == value)
        
        result = await self.session.execute(stmt)
        return result.scalar()
    
    async def exists(self, id: int) -> bool:
        """Check if a record exists by ID"""
        stmt = select(func.count(self.model.id)).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar() > 0
    
    async def get_multi_by_ids(self, ids: List[int]) -> List[ModelType]:
        """Get multiple records by IDs"""
        stmt = select(self.model).where(self.model.id.in_(ids))
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def bulk_create(self, objects: List[CreateSchemaType]) -> List[ModelType]:
        """Create multiple records in bulk"""
        db_objects = []
        for obj_in in objects:
            if hasattr(obj_in, 'dict'):
                obj_data = obj_in.dict()
            else:
                obj_data = obj_in
            
            db_obj = self.model(**obj_data)
            db_objects.append(db_obj)
        
        self.session.add_all(db_objects)
        await self.session.flush()
        
        # Refresh all objects to get generated IDs
        for db_obj in db_objects:
            await self.session.refresh(db_obj)
        
        return db_objects
    
    async def bulk_update(self, updates: List[Dict[str, Any]]) -> None:
        """Update multiple records in bulk"""
        if not updates:
            return
        
        stmt = update(self.model)
        await self.session.execute(stmt, updates)
        await self.session.flush()
    
    async def bulk_delete(self, ids: List[int]) -> None:
        """Delete multiple records in bulk"""
        stmt = delete(self.model).where(self.model.id.in_(ids))
        await self.session.execute(stmt)
        await self.session.flush()