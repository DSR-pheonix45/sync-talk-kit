from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CompanyRole(str, Enum):
    admin = "admin"
    member = "member"
    viewer = "viewer"

class CompanyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    domain: Optional[str] = Field(None, max_length=100)

class CompanyResponse(BaseModel):
    company_id: str
    name: str
    description: Optional[str]
    domain: Optional[str]
    created_at: datetime

class CompanyMemberCreate(BaseModel):
    company_id: str
    user_id: str
    role: CompanyRole

class CompanyMemberResponse(BaseModel):
    id: str
    company_id: str
    user_id: str
    role: CompanyRole
    created_at: datetime

class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    domain: Optional[str] = Field(None, max_length=100)
