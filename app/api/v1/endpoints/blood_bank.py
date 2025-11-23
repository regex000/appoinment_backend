"""Blood Bank endpoints"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.blood_bank import (
    BloodBankCreate,
    BloodBankUpdate,
    BloodBankResponse,
)
from app.crud.blood_bank import blood_bank as crud_blood_bank
from app.core.dependencies import get_current_admin_user
from app.core.exceptions import NotFoundException, ConflictException
from app.core.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(prefix="/blood-banks", tags=["blood-banks"])


@router.get("", response_model=list[BloodBankResponse])
async def list_blood_banks(
    skip: int = Query(0, ge=0),
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    active_only: bool = Query(True),
    available_24_7: bool = Query(False),
    blood_group: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    List all blood banks
    
    - **skip**: Number of records to skip
    - **limit**: Number of records to return
    - **active_only**: Return only active blood banks
    - **available_24_7**: Return only 24/7 available blood banks
    - **blood_group**: Filter by available blood group (e.g., O+, A-, B+, AB-)
    """
    if blood_group:
        banks, _ = await crud_blood_bank.get_by_blood_group(db, blood_group, skip=skip, limit=limit)
    elif available_24_7:
        banks, _ = await crud_blood_bank.get_available_24_7(db, skip=skip, limit=limit)
    else:
        filters = {"is_active": True} if active_only else None
        banks, _ = await crud_blood_bank.get_all(db, skip=skip, limit=limit, filters=filters)
    return banks


@router.get("/{bank_id}", response_model=BloodBankResponse)
async def get_blood_bank(
    bank_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get blood bank details"""
    bank = await crud_blood_bank.get(db, bank_id)
    if not bank:
        raise NotFoundException(detail="Blood bank not found")
    
    return bank


@router.post("", response_model=BloodBankResponse, status_code=201)
async def create_blood_bank(
    bank_in: BloodBankCreate,
    current_user = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new blood bank (admin only)"""
    # Check if blood bank already exists
    existing = await crud_blood_bank.get_by_name(db, bank_in.name)
    if existing:
        raise ConflictException(detail="Blood bank with this name already exists")
    
    bank = await crud_blood_bank.create(db, bank_in)
    return bank


@router.put("/{bank_id}", response_model=BloodBankResponse)
async def update_blood_bank(
    bank_id: int,
    bank_in: BloodBankUpdate,
    current_user = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Update blood bank (admin only)"""
    bank = await crud_blood_bank.get(db, bank_id)
    if not bank:
        raise NotFoundException(detail="Blood bank not found")
    
    # Check if new name already exists
    if bank_in.name and bank_in.name != bank.name:
        existing = await crud_blood_bank.get_by_name(db, bank_in.name)
        if existing:
            raise ConflictException(detail="Blood bank with this name already exists")
    
    bank = await crud_blood_bank.update(db, bank, bank_in)
    return bank


@router.delete("/{bank_id}", status_code=204)
async def delete_blood_bank(
    bank_id: int,
    current_user = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete blood bank (admin only)"""
    success = await crud_blood_bank.delete(db, bank_id)
    if not success:
        raise NotFoundException(detail="Blood bank not found")
