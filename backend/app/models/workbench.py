from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"

class WorkbenchCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    company_id: Optional[str] = None

class WorkbenchResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    owner_user_id: Optional[str]
    company_id: Optional[str]
    created_at: datetime

class WorkbenchMemberCreate(BaseModel):
    workbench_id: str
    user_id: str
    role: Role

class WorkbenchMemberResponse(BaseModel):
    id: str
    workbench_id: str
    user_id: str
    role: Role
    created_at: datetime

class WorkbenchFileCreate(BaseModel):
    file_name: str
    file_type: Optional[str] = None
    size_bytes: int

class WorkbenchFileResponse(BaseModel):
    id: str
    workbench_id: str
    storage_file_id: Optional[str]
    file_name: str
    file_type: Optional[str]
    size_bytes: int
    status: str
    error_message: Optional[str]
    created_at: datetime

class WorkbenchFileStatus(BaseModel):
    status: str
    error_message: Optional[str] = None
