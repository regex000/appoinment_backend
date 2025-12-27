"""Doctor endpoints"""

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
import os

from app.db.session import get_db
from app.db.models import Doctor
from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse,
    DoctorDetailResponse,
)
from app.crud.doctor import doctor as crud_doctor
from app.crud.department import department as crud_department
from app.core.dependencies import get_current_admin_user
from app.core.exceptions import NotFoundException, ValidationException
from app.core.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(prefix="/doctors", tags=["doctors"])


def get_absolute_image_url(image_url: str, request: Request = None) -> str:
    """
    Convert relative image URL to absolute URL pointing to the backend API.
    
    Args:
        image_url: The image URL (can be relative like /public/doctors/image.png or absolute)
        request: FastAPI Request object (optional, for getting base URL)
    
    Returns:
        Absolute URL to the image
    """
    if not image_url:
        return None
    
    # If already absolute, return as is
    if image_url.startswith("http://") or image_url.startswith("https://"):
        return image_url
    
    # Get base URL from environment or request
    if request:
        base_url = f"{request.url.scheme}://{request.url.netloc}"
    else:
        # Fallback to environment variable or default
        base_url = os.getenv("BACKEND_URL", "https://appoinment-backend-5oxs.onrender.com")
    
    # Ensure image_url starts with /
    if not image_url.startswith("/"):
        image_url = "/" + image_url
    
    return f"{base_url}{image_url}"


@router.get("", response_model=list[DoctorResponse])
async def list_doctors(
    skip: int = Query(0, ge=0),
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    department_id: int = Query(None, alias="dept"),
    specialty: str = Query(None),
    available_only: bool = Query(True),
    db: AsyncSession = Depends(get_db)
):
    """
    List all doctors
    
    - **skip**: Number of records to skip
    - **limit**: Number of records to return
    - **department_id** or **dept**: Filter by department
    - **specialty**: Filter by specialty
    - **available_only**: Return only available doctors
    """
    if department_id:
        doctors = await crud_doctor.get_by_department(db, department_id, skip, limit)
    elif specialty:
        doctors = await crud_doctor.get_by_specialty(db, specialty, skip, limit)
    elif available_only:
        doctors = await crud_doctor.get_available(db, skip, limit)
    else:
        doctors, _ = await crud_doctor.get_all(db, skip, limit)
    
    # Convert image URLs to absolute URLs
    for doctor in doctors:
        if hasattr(doctor, 'image_url') and doctor.image_url:
            doctor.image_url = get_absolute_image_url(doctor.image_url, None)
    
    return doctors


@router.get("/department/{department_id}", response_model=list[DoctorResponse])
async def get_doctors_by_department(
    department_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    db: AsyncSession = Depends(get_db)
):
    """Get doctors by department"""
    # Verify department exists
    department = await crud_department.get(db, department_id)
    if not department:
        raise NotFoundException(detail="Department not found")
    
    doctors = await crud_doctor.get_by_department(db, department_id, skip, limit)
    
    # Convert image URLs to absolute URLs
    for doctor in doctors:
        if hasattr(doctor, 'image_url') and doctor.image_url:
            doctor.image_url = get_absolute_image_url(doctor.image_url, None)
    
    return doctors


@router.get("/{doctor_id}", response_model=DoctorDetailResponse)
async def get_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get doctor details"""
    result = await db.execute(
        select(Doctor)
        .where(Doctor.id == doctor_id)
        .options(selectinload(Doctor.department), selectinload(Doctor.appointments))
    )
    doctor = result.scalars().first()
    
    if not doctor:
        raise NotFoundException(detail="Doctor not found")
    
    department = doctor.department
    
    # Convert doctor model to dict for response
    doctor_dict = {
        "id": doctor.id,
        "name": doctor.name,
        "email": doctor.email,
        "phone": doctor.phone,
        "specialty": doctor.specialty,
        "department_id": doctor.department_id,
        "image_url": get_absolute_image_url(doctor.image_url, None),
        "bio": doctor.bio,
        "experience_years": doctor.experience_years,
        "is_available": doctor.is_available,
        "profile_data": doctor.profile_data,
        "is_active": doctor.is_active,
        "created_at": doctor.created_at,
        "updated_at": doctor.updated_at,
        "department_name": department.name if department else None,
        "appointments_count": len(doctor.appointments) if doctor.appointments else 0,
    }
    
    return doctor_dict


@router.post("", response_model=DoctorResponse, status_code=201)
async def create_doctor(
    doctor_in: DoctorCreate,
    current_user = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new doctor (admin only)"""
    # Verify department exists
    department = await crud_department.get(db, doctor_in.department_id)
    if not department:
        raise NotFoundException(detail="Department not found")
    
    # Create doctor
    doctor = await crud_doctor.create(db, doctor_in)
    
    # Refresh to load relationships
    await db.refresh(doctor)
    
    return doctor


@router.put("/{doctor_id}", response_model=DoctorResponse)
async def update_doctor(
    doctor_id: int,
    doctor_in: DoctorUpdate,
    current_user = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Update doctor (admin only)"""
    doctor = await crud_doctor.get(db, doctor_id)
    if not doctor:
        raise NotFoundException(detail="Doctor not found")
    
    # Verify department if provided
    if doctor_in.department_id:
        department = await crud_department.get(db, doctor_in.department_id)
        if not department:
            raise NotFoundException(detail="Department not found")
    
    doctor = await crud_doctor.update(db, doctor, doctor_in)
    
    # Refresh to load relationships
    await db.refresh(doctor)
    
    return doctor


@router.delete("/{doctor_id}", status_code=204)
async def delete_doctor(
    doctor_id: int,
    current_user = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete doctor (admin only)"""
    doctor = await crud_doctor.get(db, doctor_id)
    if not doctor:
        raise NotFoundException(detail="Doctor not found")
    
    success = await crud_doctor.delete(db, doctor_id)
    if not success:
        raise NotFoundException(detail="Doctor not found")
    
    await db.commit()
