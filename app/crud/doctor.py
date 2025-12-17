"""Doctor CRUD operations"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import Doctor
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from .base import CRUDBase


class CRUDDoctor(CRUDBase[Doctor, DoctorCreate, DoctorUpdate]):
    """Doctor CRUD operations"""
    
    async def get_by_department(self, db: AsyncSession, department_id: int, skip: int = 0, limit: int = 100):
        """Get doctors by department"""
        result = await db.execute(
            select(Doctor)
            .where(Doctor.department_id == department_id)
            .where(Doctor.is_active == True)
            .where(Doctor.is_available == True)
            .options(selectinload(Doctor.department))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_available(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """Get all available doctors"""
        result = await db.execute(
            select(Doctor)
            .where(Doctor.is_active == True)
            .where(Doctor.is_available == True)
            .options(selectinload(Doctor.department))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_specialty(self, db: AsyncSession, specialty: str, skip: int = 0, limit: int = 100):
        """Get doctors by specialty"""
        result = await db.execute(
            select(Doctor)
            .where(Doctor.specialty.ilike(f"%{specialty}%"))
            .where(Doctor.is_active == True)
            .options(selectinload(Doctor.department))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


doctor = CRUDDoctor(Doctor)
