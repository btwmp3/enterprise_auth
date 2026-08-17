from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from app.services.policy_engine import PolicyEngine

security_scheme = HTTPBearer()

def get_current_user_context(credentials: HTTPAuthorizationCredentials = Security(security_scheme)) -> dict:
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный или истекший токен доступа",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


class PermissionChecker:
    def __init__(self, required_permission: str, abac_policy: dict | None = None):
        self.required_permission = required_permission
        self.abac_policy = abac_policy

    def __call__(
        self, 
        request: Request, 
        user_context: dict = Depends(get_current_user_context)
    ) -> dict:
        permissions = user_context.get("permissions", [])

        # Извлекаем amount из query/path параметров запроса, если он там есть
        amount_param = request.query_params.get("amount") or request.path_params.get("amount")
        amount = float(amount_param) if amount_param else 0.0

        # Собираем ПОЛНЫЙ контекст для ABAC
        context = {
            "user": {
                "department": user_context.get("department"),
                "roles": user_context.get("roles", [])
            },
            "resource": {
                "amount": amount
            },
            "environment": {
                "ip_allowed": request.client.host in ["127.0.0.1", "localhost", "testclient"]
            }
        }

        # Полный прогон через PolicyEngine (RBAC + ABAC)
        has_access = PolicyEngine.check_access(
            user_permissions=permissions,
            required_permission=self.required_permission,
            abac_policy=self.abac_policy,
            context=context
        )

        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Отказано в доступе: нарушение RBAC/ABAC политики для действия {self.required_permission}"
            )

        return user_context