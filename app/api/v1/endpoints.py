from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.domain import User, Role, Tenant
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.auth import (
    UserRegister, UserLogin, UserResponse, Token, 
    RoleCreate, RoleResponse, AssignRoleRequest, TenantCreate, TenantResponse
)
from app.api.dependencies import get_current_user_context

router = APIRouter()

# --- TENANTS ---
@router.post("/tenants", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(tenant_in: TenantCreate, db: Session = Depends(get_db)):
    db_tenant = db.query(Tenant).filter(Tenant.domain == tenant_in.domain).first()
    if db_tenant:
        raise HTTPException(status_code=400, detail="Тенент с таким доменам уже существует")
    
    tenant = Tenant(name=tenant_in.name, domain=tenant_in.domain)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

# --- AUTHENTICATION ---
@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_in.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    
    hashed_pwd = get_password_hash(user_in.password)
    user = User(
        tenant_id=user_in.tenant_id,
        email=user_in.email,
        hashed_password=hashed_pwd,
        department=user_in.department
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/auth/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    # Собираем роли и разрешения из БД
    roles = [role.name for role in user.roles]
    permissions = []
    for role in user.roles:
        permissions.extend(role.permissions)
    permissions = list(set(permissions))

    token = create_access_token(
        user_id=str(user.id),
        tenant_id=str(user.tenant_id),
        roles=roles,
        permissions=permissions,
        department=user.department
    )
    return {"access_token": token, "token_type": "bearer"}

@router.get("/auth/me")
def get_me(user_context: dict = Depends(get_current_user_context)):
    return user_context

# --- ROLE MANAGEMENT (Открытые эндпоинты для Sandbox/Dev) ---
@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    role_in: RoleCreate, 
    db: Session = Depends(get_db)
):
    role = Role(
        tenant_id=role_in.tenant_id,
        name=role_in.name,
        permissions=role_in.permissions
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

@router.post("/roles/assign")
def assign_role_to_user(
    req: AssignRoleRequest, 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == req.user_id).first()
    role = db.query(Role).filter(Role.id == req.role_id).first()
    
    if not user or not role:
        raise HTTPException(status_code=404, detail="Пользователь или роль не найдены")
    
    if role not in user.roles:
        user.roles.append(role)
        db.commit()
    
    return {"status": "success", "message": f"Роль {role.name} успешно назначена пользователю {user.email}"}