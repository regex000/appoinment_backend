"""
Department Seed Script
Seeds the database with all hospital departments
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.models import Department
from app.config import settings


# Department data with clinical and diagnostic departments
DEPARTMENTS_DATA = [
    # Clinical and Diagnostic Departments
    {
        "name": "Anesthesiology",
        "description": "Anesthesia services for surgical procedures and pain management"
    },
    {
        "name": "Cardiology",
        "description": "Heart care and cardiovascular disease treatment"
    },
    {
        "name": "Dermatology",
        "description": "Skin care and dermatological treatments"
    },
    {
        "name": "Emergency Department",
        "description": "Emergency and casualty services for acute medical conditions"
    },
    {
        "name": "Gastroenterology",
        "description": "Digestive system and gastrointestinal disease treatment"
    },
    {
        "name": "Hematology",
        "description": "Blood disorders and hematological disease treatment"
    },
    {
        "name": "Intensive Care Unit",
        "description": "Critical care services for seriously ill patients"
    },
    {
        "name": "Maternity and Neonatal Care",
        "description": "Pregnancy, childbirth, and newborn care services"
    },
    {
        "name": "Neurology",
        "description": "Nervous system disorders and neurological treatments"
    },
    {
        "name": "Obstetrics and Gynecology",
        "description": "Women's health, pregnancy, and childbirth services"
    },
    {
        "name": "Oncology",
        "description": "Cancer treatment and oncological services"
    },
    {
        "name": "Ophthalmology",
        "description": "Eye care and ophthalmological treatments"
    },
    {
        "name": "Orthopedics",
        "description": "Bone and joint disorders treatment"
    },
    {
        "name": "Pathology",
        "description": "Laboratory analysis and sample testing"
    },
    {
        "name": "Pediatrics",
        "description": "Children's health and pediatric care"
    },
    {
        "name": "Psychiatry",
        "description": "Mental health and psychiatric services"
    },
    {
        "name": "Radiology and Imaging",
        "description": "Medical imaging and radiological services"
    },
    {
        "name": "Urology",
        "description": "Urinary tract and male reproductive organ treatment"
    },
    # Support and Administrative Departments
    {
        "name": "Central Sterilization Unit",
        "description": "Sterilization and disinfection of medical equipment"
    },
    {
        "name": "Engineering Services",
        "description": "Maintenance and engineering support services"
    },
    {
        "name": "Finance",
        "description": "Financial management and billing services"
    },
    {
        "name": "Human Resources",
        "description": "Human resources and staff management"
    },
    {
        "name": "Inpatient and Outpatient Medical Records",
        "description": "Medical records management for inpatient and outpatient services"
    },
    {
        "name": "Nutrition and Dietetics",
        "description": "Nutritional counseling and dietary services"
    },
]


async def seed_departments():
    """Seed departments into the database"""
    
    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        future=True
    )
    
    # Create session factory
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    try:
        async with async_session() as session:
            print("🔍 Checking existing departments...")
            
            # Check if departments already exist
            result = await session.execute(select(Department))
            existing_departments = result.scalars().all()
            
            if existing_departments:
                print(f"⚠️  Found {len(existing_departments)} existing departments")
                print("Existing departments:")
                for dept in existing_departments:
                    print(f"  - {dept.name}")
                
                response = input("\n❓ Do you want to clear and reseed? (yes/no): ").strip().lower()
                if response == "yes":
                    print("🗑️  Deleting existing departments...")
                    await session.query(Department).delete()
                    await session.commit()
                    print("✅ Deleted existing departments")
                else:
                    print("⏭️  Skipping seed operation")
                    return
            
            print(f"\n📝 Seeding {len(DEPARTMENTS_DATA)} departments...")
            
            # Create department objects
            departments = []
            for dept_data in DEPARTMENTS_DATA:
                department = Department(
                    name=dept_data["name"],
                    description=dept_data["description"],
                    is_active=True
                )
                departments.append(department)
            
            # Add all departments to session
            session.add_all(departments)
            
            # Commit the transaction
            await session.commit()
            
            print(f"✅ Successfully seeded {len(departments)} departments!")
            print("\n📋 Seeded Departments:")
            for i, dept in enumerate(departments, 1):
                print(f"  {i}. {dept.name}")
            
    except Exception as e:
        print(f"❌ Error seeding departments: {str(e)}")
        raise
    finally:
        await engine.dispose()


async def main():
    """Main entry point"""
    print("=" * 60)
    print("🏥 Hospital Department Seed Script")
    print("=" * 60)
    print(f"Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Unknown'}")
    print("=" * 60 + "\n")
    
    await seed_departments()
    
    print("\n" + "=" * 60)
    print("✨ Seed operation completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
