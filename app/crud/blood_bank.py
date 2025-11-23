"""Blood Bank CRUD operations"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.db.models import BloodBank
from app.schemas.blood_bank import BloodBankCreate, BloodBankUpdate
from app.crud.base import CRUDBase


class CRUDBloodBank(CRUDBase[BloodBank, BloodBankCreate, BloodBankUpdate]):
    """CRUD operations for Blood Bank"""
    
    async def get_by_name(self, db: AsyncSession, name: str) -> BloodBank | None:
        """Get blood bank by name"""
        query = select(self.model).where(self.model.name == name)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_available_24_7(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 10
    ) -> tuple[list[BloodBank], int]:
        """Get 24/7 available blood banks"""
        filters = {"available_24_7": True, "is_active": True}
        return await self.get_all(db, skip=skip, limit=limit, filters=filters)
    
    async def get_by_blood_group(
        self, 
        db: AsyncSession, 
        blood_group: str,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[list[BloodBank], int]:
        """Get blood banks with available blood group"""
        # Map blood group to column name
        blood_group_map = {
            "O+": "blood_group_o_positive",
            "O-": "blood_group_o_negative",
            "A+": "blood_group_a_positive",
            "A-": "blood_group_a_negative",
            "B+": "blood_group_b_positive",
            "B-": "blood_group_b_negative",
            "AB+": "blood_group_ab_positive",
            "AB-": "blood_group_ab_negative",
        }
        
        column_name = blood_group_map.get(blood_group)
        if not column_name:
            return [], 0
        
        # Get column dynamically
        column = getattr(self.model, column_name)
        
        # Query for banks with available blood
        query = select(self.model).where(
            and_(
                column > 0,
                self.model.is_active == True
            )
        ).offset(skip).limit(limit)
        
        result = await db.execute(query)
        items = result.scalars().all()
        
        # Get total count
        count_query = select(self.model).where(
            and_(
                column > 0,
                self.model.is_active == True
            )
        )
        count_result = await db.execute(count_query)
        total = len(count_result.scalars().all())
        
        return items, total


# Create instance
blood_bank = CRUDBloodBank(BloodBank)
