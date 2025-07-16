"""
SQLAlchemy database models for MES Production Scheduling System
"""
from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Date, Boolean, DECIMAL, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from .connection import Base


class Organization(Base):
    """Organizations table"""
    __tablename__ = "organizations"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    plants: Mapped[list["Plant"]] = relationship("Plant", back_populates="organization")


class Plant(Base):
    """Plants table"""
    __tablename__ = "plants"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"))
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="plants")
    work_centers: Mapped[list["WorkCenter"]] = relationship("WorkCenter", back_populates="plant")
    
    __table_args__ = (UniqueConstraint("organization_id", "code"),)


class WorkCenterCategory(Base):
    """Work center categories table"""
    __tablename__ = "work_center_categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    default_setup_time_minutes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    work_centers: Mapped[list["WorkCenter"]] = relationship("WorkCenter", back_populates="category")


class WorkCenter(Base):
    """Work centers table"""
    __tablename__ = "work_centers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plant_id: Mapped[int] = mapped_column(Integer, ForeignKey("plants.id"))
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("work_center_categories.id"))
    capacity_hours_per_day: Mapped[float] = mapped_column(DECIMAL(4, 2), default=8.0)
    setup_time_minutes: Mapped[int] = mapped_column(Integer, default=0)
    cost_per_hour: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2))
    additional_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    plant: Mapped["Plant"] = relationship("Plant", back_populates="work_centers")
    category: Mapped[Optional["WorkCenterCategory"]] = relationship("WorkCenterCategory", back_populates="work_centers")
    operations: Mapped[list["Operation"]] = relationship("Operation", back_populates="work_center")
    
    __table_args__ = (UniqueConstraint("plant_id", "code"),)


class ProductType(Base):
    """Product types table"""
    __tablename__ = "product_types"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    type_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    can_have_children: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relationships
    products: Mapped[list["Product"]] = relationship("Product", back_populates="product_type")


class Product(Base):
    """Products table"""
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kpl: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    product_type_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("product_types.id"))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    specifications: Mapped[Optional[dict]] = mapped_column(JSONB)
    cost_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product_type: Mapped[Optional["ProductType"]] = relationship("ProductType", back_populates="products")
    work_orders: Mapped[list["WorkOrder"]] = relationship("WorkOrder", back_populates="product")


class WorkOrder(Base):
    """Work orders table"""
    __tablename__ = "work_orders"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rn: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    priority_level: Mapped[int] = mapped_column(Integer, default=0)  # HITNO field
    datum_isporuke: Mapped[Optional[date]] = mapped_column(Date)
    datum_sastavljanja: Mapped[Optional[date]] = mapped_column(Date)
    datum_treci: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="work_orders")
    operations: Mapped[list["Operation"]] = relationship("Operation", back_populates="work_order")


class Operation(Base):
    """Operations table"""
    __tablename__ = "operations"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    work_order_id: Mapped[int] = mapped_column(Integer, ForeignKey("work_orders.id"))
    work_center_id: Mapped[int] = mapped_column(Integer, ForeignKey("work_centers.id"))
    operation_sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    naziv: Mapped[str] = mapped_column(String(200), nullable=False)
    norma: Mapped[Optional[float]] = mapped_column(DECIMAL(8, 2))  # Standard time hours
    quantity: Mapped[Optional[int]] = mapped_column(Integer)
    quantity_completed: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    dependencies: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    work_order: Mapped["WorkOrder"] = relationship("WorkOrder", back_populates="operations")
    work_center: Mapped["WorkCenter"] = relationship("WorkCenter", back_populates="operations")
    
    __table_args__ = (UniqueConstraint("work_order_id", "work_center_id"),)