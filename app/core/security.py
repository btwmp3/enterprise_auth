import os
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import PyJWTError

SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_B2B_KEY_CHANGE_IN_PROD")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

hash_password = get_password_hash

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)

def create_access_token(
    user_id: str,
    tenant_id: str,
    roles: list[str],
    permissions: list[str],
    department: str | None = None,
    expires_delta: timedelta | None = None
) -> str:
    now = datetime.now(timezone.utc)
    
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    payload = {
        "sub": str(user_id),
        "tenant_id": str(tenant_id),
        "roles": roles,
        "permissions": permissions,
        "department": department,
        "exp": expire,
        "iat": now
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        return None