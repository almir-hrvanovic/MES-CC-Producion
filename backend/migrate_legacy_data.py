#!/usr/bin/env python3
"""
Migration script to transfer legacy Excel data from SQLite to PostgreSQL
"""
import asyncio
import sqlite3
from datetime import datetime
from pathlib import Path

from app.database.connection import AsyncSessionLocal
from app.database.models import Organization, Plant, WorkCenter, WorkCenterCategory, ProductType, Product, WorkOrder, Operation

# Legacy SQLite database path
LEGACY_DB_PATH = Path(__file__).parent.parent / "legacy-analysis" / "queryX.db"

async def migrate_legacy_data():
    """Migrate legacy data from SQLite to PostgreSQL"""
    print("🔄 Starting legacy data migration...")
    
    # Connect to SQLite database
    if not LEGACY_DB_PATH.exists():
        print(f"❌ Legacy database not found at {LEGACY_DB_PATH}")
        return
    
    sqlite_conn = sqlite3.connect(LEGACY_DB_PATH)
    sqlite_conn.row_factory = sqlite3.Row
    
    async with AsyncSessionLocal() as session:
        try:
            # Step 1: Create base organization and plant
            print("📋 Creating base organization and plant...")
            
            # Check if organization already exists
            from sqlalchemy import select
            org_result = await session.execute(
                select(Organization).where(Organization.code == "KEKEISEN")
            )
            org = org_result.scalar_one_or_none()
            
            if org is None:
                org = Organization(
                    code="KEKEISEN",
                    name="Kekeisen Manufacturing"
                )
                session.add(org)
                await session.flush()
                print("✅ Created organization")
            else:
                print("ℹ️  Organization already exists")
            
            # Check if plant already exists
            plant_result = await session.execute(
                select(Plant).where(Plant.code == "MAIN", Plant.organization_id == org.id)
            )
            plant = plant_result.scalar_one_or_none()
            
            if plant is None:
                plant = Plant(
                    organization_id=org.id,
                    code="MAIN",
                    name="Main Manufacturing Plant",
                    location="Main Factory",
                    is_active=True
                )
                session.add(plant)
                await session.flush()
                print("✅ Created plant")
            else:
                print("ℹ️  Plant already exists")
            
            # Step 2: Create work center categories
            print("🏭 Creating work center categories...")
            press_category = WorkCenterCategory(
                category_code="PRESS",
                category_name="Press Operations",
                description="Press brake and forming operations",
                default_setup_time_minutes=30
            )
            mill_category = WorkCenterCategory(
                category_code="MILL",
                category_name="Milling Operations", 
                description="CNC milling and machining operations",
                default_setup_time_minutes=45
            )
            session.add_all([press_category, mill_category])
            await session.flush()
            
            # Step 3: Create work centers
            print("⚙️  Creating work centers...")
            work_centers = {
                "SAV100": WorkCenter(
                    plant_id=plant.id,
                    category_id=press_category.id,
                    code="SAV100",
                    name="Press Brake SAV100",
                    description="Press brake operations",
                    capacity_hours_per_day=8,
                    setup_time_minutes=30,
                    cost_per_hour=50.00,
                    is_active=True
                ),
                "G1000": WorkCenter(
                    plant_id=plant.id,
                    category_id=mill_category.id,
                    code="G1000",
                    name="CNC Mill G1000",
                    description="CNC milling operations",
                    capacity_hours_per_day=16,
                    setup_time_minutes=45,
                    cost_per_hour=75.00,
                    is_active=True
                )
            }
            
            for wc in work_centers.values():
                session.add(wc)
            await session.flush()
            
            # Step 4: Create product types
            print("📦 Creating product types...")
            frame_type = ProductType(
                type_code="FRAME",
                type_name="Frame Components",
                description="Frame and structural components",
                can_have_children=True,
                sort_order=1
            )
            session.add(frame_type)
            await session.flush()
            
            # Step 5: Migrate products and work orders
            print("🔄 Migrating products and work orders...")
            
            # Get unique products from SQLite
            cursor = sqlite_conn.cursor()
            cursor.execute("""
                SELECT DISTINCT kpl, naziv, hitno 
                FROM work_orders 
                WHERE kpl IS NOT NULL 
                ORDER BY kpl
            """)
            
            products = {}
            for row in cursor.fetchall():
                kpl = str(row['kpl'])
                naziv = row['naziv'] or f"Product {kpl}"
                priority = row['hitno'] or 3
                
                product = Product(
                    type_id=frame_type.id,
                    kpl=kpl,
                    name=naziv[:200],  # Limit name length
                    description=f"Product {kpl}",
                    priority_level=min(priority, 3),
                    is_active=True
                )
                products[kpl] = product
                session.add(product)
            
            await session.flush()
            print(f"✅ Created {len(products)} products")
            
            # Step 6: Migrate operations
            print("🔧 Migrating operations...")
            
            cursor.execute("""
                SELECT * FROM work_orders ORDER BY kpl, rn
            """)
            
            operations_created = 0
            work_orders_created = 0
            current_work_order = None
            
            for row in cursor.fetchall():
                kpl = str(row['kpl'])
                if kpl not in products:
                    continue
                
                # Create work order if it doesn't exist for this product
                if current_work_order is None or current_work_order.product_id != products[kpl].id:
                    work_order = WorkOrder(
                        product_id=products[kpl].id,
                        rn=f"WO-{kpl}",
                        quantity=row['quantity'] or 1,
                        priority_level=row['hitno'] or 3,
                        datum_isporuke=datetime.strptime(row['datum_isporuke'], '%Y-%m-%d').date() if row['datum_isporuke'] else None,
                        datum_sastavljanja=datetime.strptime(row['datum_sastavljanja'], '%Y-%m-%d').date() if row['datum_sastavljanja'] else None,
                        datum_treci=datetime.strptime(row['zavrsetak_masinske'], '%Y-%m-%d').date() if row['zavrsetak_masinske'] else None,
                        status="pending",
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    session.add(work_order)
                    await session.flush()
                    current_work_order = work_order
                    work_orders_created += 1
                
                # Create operation
                wc_code = row['wc'] or 'SAV100'
                if wc_code not in work_centers:
                    wc_code = 'SAV100'  # Default fallback
                
                operation = Operation(
                    work_order_id=current_work_order.id,
                    work_center_id=work_centers[wc_code].id,
                    operation_sequence=row['rn'] or operations_created + 1,
                    naziv=row['naziv'] or f"Operation {row['rn']}",
                    norma=float(row['norma']) if row['norma'] else 0.0,
                    quantity=row['quantity'] or 1,
                    quantity_completed=row['cq'] or 0,
                    status="pending",
                    estimated_start_time=datetime.utcnow(),
                    estimated_completion_time=datetime.utcnow()
                )
                session.add(operation)
                operations_created += 1
            
            await session.commit()
            print(f"✅ Created {work_orders_created} work orders")
            print(f"✅ Created {operations_created} operations")
            
            # Step 7: Display migration summary
            print("\n📊 Migration Summary:")
            print(f"  • Organization: {org.name}")
            print(f"  • Plant: {plant.name}")
            print(f"  • Work Centers: {len(work_centers)}")
            print(f"  • Products: {len(products)}")
            print(f"  • Work Orders: {work_orders_created}")
            print(f"  • Operations: {operations_created}")
            
            print("\n✅ Legacy data migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            await session.rollback()
            raise
        finally:
            sqlite_conn.close()

if __name__ == "__main__":
    asyncio.run(migrate_legacy_data())