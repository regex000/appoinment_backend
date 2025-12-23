"""Department endpoints"""

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
import os

from app.db.session import get_db
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    DepartmentDetailResponse,
)
from app.crud.department import department as crud_department
from app.core.dependencies import get_current_admin_user
from app.core.exceptions import NotFoundException, ConflictException
from app.core.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(prefix="/departments", tags=["departments"])


def get_absolute_image_url(image_url: str, request: Request = None) -> str:
    """
    Convert relative image URL to absolute URL pointing to the backend API.
    
    Args:
        image_url: The image URL (can be relative like /public/departments/image.svg or absolute)
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


@router.get("", response_model=list[DepartmentResponse])
async def list_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    active_only: bool = Query(True),
    db: AsyncSession = Depends(get_db)
):
    """
    List all departments
    
    - **skip**: Number of records to skip
    - **limit**: Number of records to return
    - **active_only**: Return only active departments
    """
    filters = {"is_active": True} if active_only else None
    departments, _ = await crud_department.get_all(db, skip=skip, limit=limit, filters=filters)
    
    # Convert image URLs to absolute URLs
    for department in departments:
        if hasattr(department, 'image_url') and department.image_url:
            department.image_url = get_absolute_image_url(department.image_url, None)
    
    return departments


@router.get("/{department_id}", response_model=DepartmentDetailResponse)
async def get_department(
    department_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get department details"""
    department = await crud_department.get(db, department_id)
    if not department:
        raise NotFoundException(detail="Department not found")
    
    # Get doctors count
    doctors_count = len(department.doctors) if department.doctors else 0
    
    dept_dict = DepartmentResponse.from_orm(department).dict()
    
    # Convert image URL to absolute URL
    if dept_dict.get('image_url'):
        dept_dict['image_url'] = get_absolute_image_url(dept_dict['image_url'], None)
    
    return {
        **dept_dict,
        "doctors_count": doctors_count
    }


@router.post("", response_model=DepartmentResponse, status_code=201)
async def create_department(
    department_in: DepartmentCreate,
    current_user = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new department (admin only)"""
    # Check if department already exists
    existing = await crud_department.get_by_name(db, department_in.name)
    if existing:
        raise ConflictException(detail="Department with this name already exists")
    
    department = await crud_department.create(db, department_in)
    
    # Convert image URL to absolute URL
    if hasattr(department, 'image_url') and department.image_url:
        department.image_url = get_absolute_image_url(department.image_url, None)
    
    return department


@router.put("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: int,
    department_in: DepartmentUpdate,
    current_user = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Update department (admin only)"""
    department = await crud_department.get(db, department_id)
    if not department:
        raise NotFoundException(detail="Department not found")
    
    # Check if new name already exists
    if department_in.name and department_in.name != department.name:
        existing = await crud_department.get_by_name(db, department_in.name)
        if existing:
            raise ConflictException(detail="Department with this name already exists")
    
    department = await crud_department.update(db, department, department_in)
    
    # Convert image URL to absolute URL
    if hasattr(department, 'image_url') and department.image_url:
        department.image_url = get_absolute_image_url(department.image_url, None)
    
    return department


@router.delete("/{department_id}", status_code=204)
async def delete_department(
    department_id: int,
    current_user = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete department (admin only)"""
    success = await crud_department.delete(db, department_id)
    if not success:
        raise NotFoundException(detail="Department not found")
