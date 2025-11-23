"""Blood Bank schemas"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BloodBankBase(BaseModel):
    """Base Blood Bank schema"""
    name: str = Field(..., min_length=1, max_length=255, description="Blood bank name")
    description: Optional[str] = Field(None, description="Blood bank description")
    phone: str = Field(..., min_length=10, max_length=20, description="Contact phone number")
    location: Optional[str] = Field(None, max_length=500, description="Physical location")
    latitude: Optional[str] = Field(None, max_length=50, description="Latitude coordinate")
    longitude: Optional[str] = Field(None, max_length=50, description="Longitude coordinate")
    available_24_7: bool = Field(True, description="Available 24/7")


class BloodInventory(BaseModel):
    """Blood inventory schema"""
    blood_group_o_positive: int = Field(0, ge=0, description="O+ blood units")
    blood_group_o_negative: int = Field(0, ge=0, description="O- blood units")
    blood_group_a_positive: int = Field(0, ge=0, description="A+ blood units")
    blood_group_a_negative: int = Field(0, ge=0, description="A- blood units")
    blood_group_b_positive: int = Field(0, ge=0, description="B+ blood units")
    blood_group_b_negative: int = Field(0, ge=0, description="B- blood units")
    blood_group_ab_positive: int = Field(0, ge=0, description="AB+ blood units")
    blood_group_ab_negative: int = Field(0, ge=0, description="AB- blood units")


class BloodBankCreate(BloodBankBase, BloodInventory):
    """Create Blood Bank schema"""
    pass


class BloodBankUpdate(BaseModel):
    """Update Blood Bank schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    location: Optional[str] = Field(None, max_length=500)
    latitude: Optional[str] = Field(None, max_length=50)
    longitude: Optional[str] = Field(None, max_length=50)
    available_24_7: Optional[bool] = None
    blood_group_o_positive: Optional[int] = Field(None, ge=0)
    blood_group_o_negative: Optional[int] = Field(None, ge=0)
    blood_group_a_positive: Optional[int] = Field(None, ge=0)
    blood_group_a_negative: Optional[int] = Field(None, ge=0)
    blood_group_b_positive: Optional[int] = Field(None, ge=0)
    blood_group_b_negative: Optional[int] = Field(None, ge=0)
    blood_group_ab_positive: Optional[int] = Field(None, ge=0)
    blood_group_ab_negative: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class BloodBankResponse(BloodBankBase, BloodInventory):
    """Blood Bank response schema"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
