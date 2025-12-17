"""Doctor schemas"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class DoctorBase(BaseModel):
    """Base doctor schema"""
    name: str = Field(..., min_length=1, max_length=255, description="Doctor name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    specialty: str = Field(..., min_length=1, max_length=255, description="Medical specialty")
    department_id: int = Field(..., description="Department ID")
    image_url: Optional[str] = Field(None, description="Doctor image URL")
    bio: Optional[str] = Field(None, description="Doctor biography")
    experience_years: Optional[int] = Field(None, ge=0, description="Years of experience")
    is_available: Optional[bool] = Field(True, description="Is doctor available")
    profile_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Flexible profile data (JSON)")


class DoctorCreate(DoctorBase):
    """Doctor creation schema"""
    pass


class DoctorUpdate(BaseModel):
    """Doctor update schema"""
    name: Optional[str] = Field(None, max_length=255)
    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None, max_length=20)
    specialty: Optional[str] = Field(None, max_length=255)
    department_id: Optional[int] = Field(None)
    image_url: Optional[str] = Field(None)
    bio: Optional[str] = Field(None)
    experience_years: Optional[int] = Field(None, ge=0)
    is_available: Optional[bool] = Field(None)
    profile_data: Optional[Dict[str, Any]] = Field(None, description="Flexible profile data (JSON)")


class DoctorResponse(DoctorBase):
    """Doctor response schema"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DoctorDetailResponse(DoctorResponse):
    """Doctor detail response with department info"""
    department_name: Optional[str] = None
    appointments_count: int = 0
