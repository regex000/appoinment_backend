#!/usr/bin/env python3
"""
Comprehensive data seeding script for Modern Hospital Management System
Seeds: Departments, Services, Ambulance Services, Eye Products, and additional Doctors
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import AsyncSessionLocal, init_db
from app.db.models import (
    Department, Service, AmbulanceService, EyeProduct, Doctor, User
)
from app.core.security import SecurityUtils


# Sample data
DEPARTMENTS_DATA = [
    {
        "name": "Cardiology",
        "description": "Heart and cardiovascular diseases treatment",
        "image_url": "https://via.placeholder.com/300x200?text=Cardiology"
    },
    {
        "name": "Neurology",
        "description": "Brain and nervous system disorders",
        "image_url": "https://via.placeholder.com/300x200?text=Neurology"
    },
    {
        "name": "Orthopedics",
        "description": "Bone, joint, and muscle disorders",
        "image_url": "https://via.placeholder.com/300x200?text=Orthopedics"
    },
    {
        "name": "Pediatrics",
        "description": "Medical care for children and infants",
        "image_url": "https://via.placeholder.com/300x200?text=Pediatrics"
    },
    {
        "name": "Dentistry",
        "description": "Dental care and oral health",
        "image_url": "https://via.placeholder.com/300x200?text=Dentistry"
    },
    {
        "name": "Dermatology",
        "description": "Skin diseases and conditions",
        "image_url": "https://via.placeholder.com/300x200?text=Dermatology"
    },
    {
        "name": "Ophthalmology",
        "description": "Eye diseases and vision care",
        "image_url": "https://via.placeholder.com/300x200?text=Ophthalmology"
    },
    {
        "name": "Psychiatry",
        "description": "Mental health and psychological disorders",
        "image_url": "https://via.placeholder.com/300x200?text=Psychiatry"
    },
]

SERVICES_DATA = [
    {
        "name": "Emergency Care",
        "description": "24/7 emergency medical services",
        "icon": "🚑"
    },
    {
        "name": "Outpatient Services",
        "description": "Non-emergency medical consultations",
        "icon": "👨‍⚕️"
    },
    {
        "name": "Inpatient Services",
        "description": "Hospital admission and overnight care",
        "icon": "🏥"
    },
    {
        "name": "Diagnostic Services",
        "description": "Lab tests, X-rays, and imaging",
        "icon": "🔬"
    },
    {
        "name": "Surgery Services",
        "description": "Surgical procedures and operations",
        "icon": "🏨"
    },
    {
        "name": "Pharmacy Services",
        "description": "Prescription and over-the-counter medications",
        "icon": "💊"
    },
    {
        "name": "Rehabilitation Services",
        "description": "Physical therapy and recovery programs",
        "icon": "🏃"
    },
    {
        "name": "Maternity Services",
        "description": "Pregnancy and childbirth care",
        "icon": "👶"
    },
]

AMBULANCE_SERVICES_DATA = [
    {
        "name": "Nazmul Alom Medical Ambulance",
        "description": "Primary ambulance service with advanced life support",
        "phone": "+8801700000001",
        "location": "Dhaka, Bangladesh",
        "latitude": "23.8103",
        "longitude": "90.4125",
        "available_24_7": True,
        "ambulance_count": 5
    },
    {
        "name": "Emergency Response Ambulance",
        "description": "Rapid response emergency ambulance service",
        "phone": "+8801700000002",
        "location": "Dhaka, Bangladesh",
        "latitude": "23.8103",
        "longitude": "90.4125",
        "available_24_7": True,
        "ambulance_count": 3
    },
    {
        "name": "Medical Transport Service",
        "description": "Non-emergency patient transport",
        "phone": "+8801700000003",
        "location": "Dhaka, Bangladesh",
        "latitude": "23.8103",
        "longitude": "90.4125",
        "available_24_7": False,
        "ambulance_count": 2
    },
    {
        "name": "Critical Care Ambulance",
        "description": "ICU-equipped ambulance for critical patients",
        "phone": "+8801700000004",
        "location": "Dhaka, Bangladesh",
        "latitude": "23.8103",
        "longitude": "90.4125",
        "available_24_7": True,
        "ambulance_count": 2
    },
    {
        "name": "Pediatric Ambulance Service",
        "description": "Specialized ambulance for children",
        "phone": "+8801700000005",
        "location": "Dhaka, Bangladesh",
        "latitude": "23.8103",
        "longitude": "90.4125",
        "available_24_7": True,
        "ambulance_count": 1
    },
]

EYE_PRODUCTS_DATA = [
    # Sunglasses
    {
        "name": "Classic UV Protection Sunglasses",
        "description": "Premium sunglasses with 100% UV protection",
        "category": "Sunglasses",
        "brand": "RayBan",
        "price": "৳ 3,500",
        "stock_quantity": 25,
        "image_url": "https://via.placeholder.com/300x200?text=Sunglasses+1"
    },
    {
        "name": "Polarized Aviator Sunglasses",
        "description": "Polarized lenses reduce glare and reflections",
        "category": "Sunglasses",
        "brand": "Oakley",
        "price": "৳ 4,200",
        "stock_quantity": 18,
        "image_url": "https://via.placeholder.com/300x200?text=Sunglasses+2"
    },
    {
        "name": "Wayfarer Style Sunglasses",
        "description": "Classic wayfarer design with anti-reflective coating",
        "category": "Sunglasses",
        "brand": "RayBan",
        "price": "৳ 3,800",
        "stock_quantity": 22,
        "image_url": "https://via.placeholder.com/300x200?text=Sunglasses+3"
    },
    {
        "name": "Sports Performance Sunglasses",
        "description": "Lightweight sunglasses for sports and outdoor activities",
        "category": "Sunglasses",
        "brand": "Nike",
        "price": "৳ 2,800",
        "stock_quantity": 30,
        "image_url": "https://via.placeholder.com/300x200?text=Sunglasses+4"
    },
    
    # Contact Lenses
    {
        "name": "Daily Disposable Contact Lenses",
        "description": "Comfortable daily wear contact lenses (30 pairs)",
        "category": "Contact Lenses",
        "brand": "Acuvue",
        "price": "৳ 1,200",
        "stock_quantity": 50,
        "image_url": "https://via.placeholder.com/300x200?text=Contact+Lenses+1"
    },
    {
        "name": "Monthly Contact Lenses",
        "description": "Reusable monthly contact lenses (6 pairs)",
        "category": "Contact Lenses",
        "brand": "Bausch+Lomb",
        "price": "৳ 1,500",
        "stock_quantity": 40,
        "image_url": "https://via.placeholder.com/300x200?text=Contact+Lenses+2"
    },
    {
        "name": "Colored Contact Lenses",
        "description": "Cosmetic colored contact lenses (30 pairs)",
        "category": "Contact Lenses",
        "brand": "FreshLook",
        "price": "৳ 2,000",
        "stock_quantity": 35,
        "image_url": "https://via.placeholder.com/300x200?text=Contact+Lenses+3"
    },
    {
        "name": "Toric Contact Lenses for Astigmatism",
        "description": "Specialized lenses for astigmatism correction",
        "category": "Contact Lenses",
        "brand": "Acuvue",
        "price": "৳ 1,800",
        "stock_quantity": 25,
        "image_url": "https://via.placeholder.com/300x200?text=Contact+Lenses+4"
    },
    
    # Eye Drops
    {
        "name": "Artificial Tear Eye Drops",
        "description": "Lubricating eye drops for dry eyes (10ml)",
        "category": "Eye Drops",
        "brand": "Systane",
        "price": "৳ 350",
        "stock_quantity": 100,
        "image_url": "https://via.placeholder.com/300x200?text=Eye+Drops+1"
    },
    {
        "name": "Antihistamine Eye Drops",
        "description": "Relief for allergic eye symptoms (10ml)",
        "category": "Eye Drops",
        "brand": "Alomide",
        "price": "৳ 450",
        "stock_quantity": 80,
        "image_url": "https://via.placeholder.com/300x200?text=Eye+Drops+2"
    },
    {
        "name": "Redness Relief Eye Drops",
        "description": "Fast-acting redness relief (15ml)",
        "category": "Eye Drops",
        "brand": "Visine",
        "price": "৳ 400",
        "stock_quantity": 90,
        "image_url": "https://via.placeholder.com/300x200?text=Eye+Drops+3"
    },
    {
        "name": "Vitamin A Eye Drops",
        "description": "Nutritive eye drops with vitamin A (10ml)",
        "category": "Eye Drops",
        "brand": "Refresh",
        "price": "৳ 500",
        "stock_quantity": 70,
        "image_url": "https://via.placeholder.com/300x200?text=Eye+Drops+4"
    },
    
    # Eyeglasses Frames
    {
        "name": "Metal Frame Eyeglasses",
        "description": "Durable metal frames with adjustable nose pads",
        "category": "Frames",
        "brand": "Titan",
        "price": "৳ 2,500",
        "stock_quantity": 40,
        "image_url": "https://via.placeholder.com/300x200?text=Frames+1"
    },
    {
        "name": "Plastic Frame Eyeglasses",
        "description": "Lightweight plastic frames in various colors",
        "category": "Frames",
        "brand": "Fastrack",
        "price": "৳ 1,800",
        "stock_quantity": 50,
        "image_url": "https://via.placeholder.com/300x200?text=Frames+2"
    },
    {
        "name": "Rimless Eyeglasses",
        "description": "Modern rimless design for minimalist look",
        "category": "Frames",
        "brand": "Silhouette",
        "price": "৳ 3,200",
        "stock_quantity": 30,
        "image_url": "https://via.placeholder.com/300x200?text=Frames+3"
    },
    {
        "name": "Cat-Eye Frame Eyeglasses",
        "description": "Trendy cat-eye style frames",
        "category": "Frames",
        "brand": "Vogue",
        "price": "৳ 2,200",
        "stock_quantity": 35,
        "image_url": "https://via.placeholder.com/300x200?text=Frames+4"
    },
    
    # Lens Accessories
    {
        "name": "Lens Cleaning Solution",
        "description": "Multi-purpose lens cleaning solution (120ml)",
        "category": "Accessories",
        "brand": "Bausch+Lomb",
        "price": "৳ 250",
        "stock_quantity": 150,
        "image_url": "https://via.placeholder.com/300x200?text=Accessories+1"
    },
    {
        "name": "Microfiber Lens Cloth",
        "description": "Premium microfiber cloth for lens cleaning",
        "category": "Accessories",
        "brand": "Generic",
        "price": "৳ 150",
        "stock_quantity": 200,
        "image_url": "https://via.placeholder.com/300x200?text=Accessories+2"
    },
    {
        "name": "Eyeglass Case",
        "description": "Protective hard case for eyeglasses",
        "category": "Accessories",
        "brand": "Generic",
        "price": "৳ 300",
        "stock_quantity": 120,
        "image_url": "https://via.placeholder.com/300x200?text=Accessories+3"
    },
    {
        "name": "Contact Lens Solution",
        "description": "All-in-one contact lens solution (240ml)",
        "category": "Accessories",
        "brand": "Renu",
        "price": "৳ 400",
        "stock_quantity": 100,
        "image_url": "https://via.placeholder.com/300x200?text=Accessories+4"
    },
]

ADDITIONAL_DOCTORS_DATA = [
    {
        "phone": "+11234567893",
        "password": "Doctor@123",
        "full_name": "Dr. Michael Johnson",
        "email": "michael.johnson@hospital.com",
        "specialty": "Neurology",
        "bio": "Experienced neurologist specializing in brain disorders",
        "experience_years": 12,
        "department_name": "Neurology"
    },
    {
        "phone": "+11234567894",
        "password": "Doctor@123",
        "full_name": "Dr. Emily Davis",
        "email": "emily.davis@hospital.com",
        "specialty": "Orthopedics",
        "bio": "Orthopedic surgeon with expertise in joint replacement",
        "experience_years": 8,
        "department_name": "Orthopedics"
    },
    {
        "phone": "+11234567895",
        "password": "Doctor@123",
        "full_name": "Dr. Robert Wilson",
        "email": "robert.wilson@hospital.com",
        "specialty": "Pediatrics",
        "bio": "Pediatrician dedicated to children's health",
        "experience_years": 10,
        "department_name": "Pediatrics"
    },
    {
        "phone": "+11234567896",
        "password": "Doctor@123",
        "full_name": "Dr. Jennifer Brown",
        "email": "jennifer.brown@hospital.com",
        "specialty": "Dentistry",
        "bio": "Cosmetic and general dentist",
        "experience_years": 7,
        "department_name": "Dentistry"
    },
    {
        "phone": "+11234567897",
        "password": "Doctor@123",
        "full_name": "Dr. David Martinez",
        "email": "david.martinez@hospital.com",
        "specialty": "Dermatology",
        "bio": "Dermatologist specializing in skin conditions",
        "experience_years": 9,
        "department_name": "Dermatology"
    },
    {
        "phone": "+11234567898",
        "password": "Doctor@123",
        "full_name": "Dr. Lisa Anderson",
        "email": "lisa.anderson@hospital.com",
        "specialty": "Ophthalmology",
        "bio": "Eye specialist with expertise in vision correction",
        "experience_years": 11,
        "department_name": "Ophthalmology"
    },
    {
        "phone": "+11234567899",
        "password": "Doctor@123",
        "full_name": "Dr. James Taylor",
        "email": "james.taylor@hospital.com",
        "specialty": "Psychiatry",
        "bio": "Psychiatrist specializing in mental health treatment",
        "experience_years": 13,
        "department_name": "Psychiatry"
    },
]


async def seed_departments(session: AsyncSession):
    """Seed departments"""
    print("\n📝 Seeding Departments...")
    
    for dept_data in DEPARTMENTS_DATA:
        # Check if department already exists
        existing = await session.execute(
            select(Department).where(Department.name == dept_data["name"])
        )
        if existing.scalars().first():
            print(f"  ⚠️  Department '{dept_data['name']}' already exists")
            continue
        
        department = Department(**dept_data)
        session.add(department)
        print(f"  ✓ Created: {dept_data['name']}")
    
    await session.flush()
    print(f"✓ {len(DEPARTMENTS_DATA)} departments processed")


async def seed_services(session: AsyncSession):
    """Seed services"""
    print("\n📝 Seeding Services...")
    
    for service_data in SERVICES_DATA:
        # Check if service already exists
        existing = await session.execute(
            select(Service).where(Service.name == service_data["name"])
        )
        if existing.scalars().first():
            print(f"  ⚠️  Service '{service_data['name']}' already exists")
            continue
        
        service = Service(**service_data)
        session.add(service)
        print(f"  ✓ Created: {service_data['name']}")
    
    await session.flush()
    print(f"✓ {len(SERVICES_DATA)} services processed")


async def seed_ambulance_services(session: AsyncSession):
    """Seed ambulance services"""
    print("\n📝 Seeding Ambulance Services...")
    
    for ambulance_data in AMBULANCE_SERVICES_DATA:
        # Check if ambulance service already exists
        existing = await session.execute(
            select(AmbulanceService).where(AmbulanceService.name == ambulance_data["name"])
        )
        if existing.scalars().first():
            print(f"  ⚠️  Ambulance Service '{ambulance_data['name']}' already exists")
            continue
        
        ambulance = AmbulanceService(**ambulance_data)
        session.add(ambulance)
        print(f"  ✓ Created: {ambulance_data['name']}")
    
    await session.flush()
    print(f"✓ {len(AMBULANCE_SERVICES_DATA)} ambulance services processed")


async def seed_eye_products(session: AsyncSession):
    """Seed eye products"""
    print("\n📝 Seeding Eye Products...")
    
    for product_data in EYE_PRODUCTS_DATA:
        # Check if product already exists
        existing = await session.execute(
            select(EyeProduct).where(EyeProduct.name == product_data["name"])
        )
        if existing.scalars().first():
            print(f"  ⚠️  Product '{product_data['name']}' already exists")
            continue
        
        product = EyeProduct(**product_data, is_available=True, is_active=True)
        session.add(product)
        print(f"  ✓ Created: {product_data['name']}")
    
    await session.flush()
    print(f"✓ {len(EYE_PRODUCTS_DATA)} eye products processed")


async def seed_additional_doctors(session: AsyncSession):
    """Seed additional doctors"""
    print("\n📝 Seeding Additional Doctors...")
    
    for doctor_data in ADDITIONAL_DOCTORS_DATA:
        # Check if user already exists
        existing_user = await session.execute(
            select(User).where(User.phone == doctor_data["phone"])
        )
        if existing_user.scalars().first():
            print(f"  ⚠️  Doctor '{doctor_data['full_name']}' already exists")
            continue
        
        # Get department
        dept_result = await session.execute(
            select(Department).where(Department.name == doctor_data["department_name"])
        )
        department = dept_result.scalars().first()
        
        if not department:
            print(f"  ✗ Department '{doctor_data['department_name']}' not found")
            continue
        
        # Create user
        user = User(
            phone=doctor_data["phone"],
            hashed_password=SecurityUtils.get_password_hash(doctor_data["password"]),
            full_name=doctor_data["full_name"],
            email=doctor_data["email"],
            is_active=True,
            is_admin=False,
            is_doctor=True,
        )
        session.add(user)
        await session.flush()
        
        # Create doctor profile
        doctor = Doctor(
            user_id=user.id,
            specialty=doctor_data["specialty"],
            bio=doctor_data["bio"],
            experience_years=doctor_data["experience_years"],
            department_id=department.id,
            is_available=True,
        )
        session.add(doctor)
        await session.flush()
        
        print(f"  ✓ Created: {doctor_data['full_name']} ({doctor_data['specialty']})")
    
    print(f"✓ {len(ADDITIONAL_DOCTORS_DATA)} doctors processed")


async def seed_all_data():
    """Seed all data"""
    print("="*70)
    print("🌱 MODERN HOSPITAL MANAGEMENT SYSTEM - DATA SEEDING")
    print("="*70)
    
    # Initialize database
    print("\n🔧 Initializing database...")
    await init_db()
    print("✓ Database initialized")
    
    async with AsyncSessionLocal() as session:
        try:
            # Seed all data
            await seed_departments(session)
            await seed_services(session)
            await seed_ambulance_services(session)
            await seed_eye_products(session)
            await seed_additional_doctors(session)
            
            # Commit all changes
            await session.commit()
            
            print("\n" + "="*70)
            print("✅ ALL DATA SEEDED SUCCESSFULLY!")
            print("="*70)
            
            # Print summary
            print("\n📊 SEEDING SUMMARY:\n")
            print(f"  • Departments: {len(DEPARTMENTS_DATA)}")
            print(f"  • Services: {len(SERVICES_DATA)}")
            print(f"  • Ambulance Services: {len(AMBULANCE_SERVICES_DATA)}")
            print(f"  • Eye Products: {len(EYE_PRODUCTS_DATA)}")
            print(f"  • Additional Doctors: {len(ADDITIONAL_DOCTORS_DATA)}")
            
            total_items = (
                len(DEPARTMENTS_DATA) +
                len(SERVICES_DATA) +
                len(AMBULANCE_SERVICES_DATA) +
                len(EYE_PRODUCTS_DATA) +
                len(ADDITIONAL_DOCTORS_DATA)
            )
            print(f"\n  📈 Total Items Seeded: {total_items}")
            
            print("\n" + "="*70)
            print("🎯 NEXT STEPS:")
            print("="*70)
            print("\n1. Test API endpoints:")
            print("   - GET /api/v1/departments")
            print("   - GET /api/v1/services")
            print("   - GET /api/v1/ambulance-services")
            print("   - GET /api/v1/eye-products")
            print("   - GET /api/v1/doctors")
            print("\n2. Login with doctor credentials:")
            print("   - Phone: +11234567893 (Dr. Michael Johnson)")
            print("   - Password: Doctor@123")
            print("\n3. Access API documentation:")
            print("   - https://appoinment-backend-gy1s.onrender.com/docs")
            print("\n" + "="*70 + "\n")
            
        except Exception as e:
            await session.rollback()
            print(f"\n❌ Error seeding data: {e}")
            raise


async def main():
    """Main entry point"""
    try:
        await seed_all_data()
    except Exception as e:
        print(f"\n❌ Failed to seed data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
