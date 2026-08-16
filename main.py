from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.dependencies import PermissionChecker
from app.api.v1.endpoints import router as api_router

# Объявляем схему авторизации через Bearer-токен для Swagger
security_scheme = HTTPBearer()

app = FastAPI(
    title="Enterprise B2B Auth & Policy Service",
    description="Multi-tenant RBAC + ABAC Authorization Microservice",
    version="1.0.0",
    swagger_ui_parameters={"persistAuthorization": True}
)

# Раздаем статические файлы фронтенда
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем API v1 (/auth, /tenants, /roles)
app.include_router(api_router, prefix="/api/v1")

INVOICE_APPROVE_POLICY = {
    "rules": {
        "user.department": {"eq": "Finance"},
        "resource.amount": {"lte": 10000}
    }
}

# Отдаем красивый UI интерактивного стенда по корневому адресу "/"
@app.get("/", include_in_schema=False)
def read_root():
    return FileResponse("static/index.html")

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok", "service": "B2B Auth Engine"}

@app.post("/api/v1/invoices/{invoice_id}/approve", tags=["Business Logic Example"]) 
def approve_invoice(
    invoice_id: str,
    amount: float,
    user_context: dict = Depends(
        PermissionChecker(
            required_permission="invoices:approve",
            abac_policy=INVOICE_APPROVE_POLICY
        )
    )
):
    return {
        "status": "success", 
        "message": f"Invoice {invoice_id} for amount {amount} successfully approved by user from {user_context.get('department')} department."
    }