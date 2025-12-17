"""
Services Seed Script
Seeds the database with hospital services
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

from app.db.models import Service
from app.config import settings


# Services data
SERVICES_DATA = [
    {
        "name": "Emergency",
        "description": "24/7 Emergency and casualty services for acute medical conditions and emergencies"
    },
    {
        "name": "Indoor",
        "description": "Inpatient hospitalization and indoor ward services"
    },
    {
        "name": "Outdoor",
        "description": "Outpatient clinic and outdoor consultation services"
    },
    {
        "name": "Pathology",
        "description": "Laboratory testing and pathological analysis services"
    },
    {
        "name": "Ophthalmology",
        "description": "Eye care and ophthalmological services"
    },
    {
        "name": "Pharmacy",
        "description": "Pharmaceutical services and medication dispensing"
    },
]


async def seed_services():
    """Seed services into the database"""
    
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
            print("🔍 Checking existing services...")
            
            # Check if services already exist
            result = await session.execute(select(Service))
            existing_services = result.scalars().all()
            
            if existing_services:
                print(f"⚠️  Found {len(existing_services)} existing services")
                print("Existing services:")
                for service in existing_services:
                    print(f"  - {service.name}")
                
                response = input("\n❓ Do you want to clear and reseed? (yes/no): ").strip().lower()
                if response == "yes":
                    print("🗑️  Deleting existing services...")
                    await session.query(Service).delete()
                    await session.commit()
                    print("✅ Deleted existing services")
                else:
                    print("⏭️  Skipping seed operation")
                    return
            
            print(f"\n📝 Seeding {len(SERVICES_DATA)} services...")
            
            # Create service objects
            services = []
            for service_data in SERVICES_DATA:
                service = Service(
                    name=service_data["name"],
                    description=service_data["description"],
                    is_active=True
                )
                services.append(service)
            
            # Add all services to session
            session.add_all(services)
            
            # Commit the transaction
            await session.commit()
            
            print(f"✅ Successfully seeded {len(services)} services!")
            print("\n📋 Seeded Services:")
            for i, service in enumerate(services, 1):
                print(f"  {i}. {service.name}")
            
    except Exception as e:
        print(f"❌ Error seeding services: {str(e)}")
        raise
    finally:
        await engine.dispose()


async def main():
    """Main entry point"""
    print("=" * 60)
    print("🏥 Hospital Services Seed Script")
    print("=" * 60)
    print(f"Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Unknown'}")
    print("=" * 60 + "\n")
    
    await seed_services()
    
    print("\n" + "=" * 60)
    print("✨ Seed operation completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
