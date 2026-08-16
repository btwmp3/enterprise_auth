from pydantic import BaseModel, EmailStr
from uuid import UUID

# Tenant Schemas
class TenantCreate(BaseModel):
    name: str
    domain: str

class TenantResponse(BaseModel):
    id: UUID
    name: str
    domain: str
    is_active: bool

    class Config:
        from_attributes = True

# User Schemas
class UserRegister(BaseModel):
    tenant_id: UUID
    email: EmailStr
    password: str
    department: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    email: str
    department: str | None
    is_active: bool
    roles: list[str] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Role Schemas
class RoleCreate(BaseModel):
    tenant_id: UUID
    name: str
    permissions: list[str] = []

class RoleResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    permissions: list[str]

    class Config:
        from_attributes = True

class AssignRoleRequest(BaseModel):
    user_id: UUID
    role_id: UUID