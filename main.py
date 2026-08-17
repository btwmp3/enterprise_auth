import os
from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.dependencies import PermissionChecker
from app.api.v1.endpoints import router as api_router

security_scheme = HTTPBearer()

app = FastAPI(
    title="Enterprise B2B Auth & Policy Service",
    description="Multi-tenant RBAC + ABAC Authorization Microservice",
    version="1.0.0",
    swagger_ui_parameters={"persistAuthorization": True}
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
def read_root():
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    return FileResponse(html_path)


@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok", "service": "B2B Auth Engine"}


@app.post("/api/v1/invoices/{invoice_id}/approve", tags=["Business Logic Example"])
def approve_invoice(
    invoice_id: str,
    amount: float,
    required_dept: str = Query("Finance", description="Required ABAC department"),
    max_amount: float = Query(10000.0, description="Max allowed amount"),
    # СТРОГАЯ ПРОВЕРКА RBAC: Без права "invoices:approve" запрос не пройдет!
    user_context: dict = Depends(
        PermissionChecker(required_permission="invoices:approve")
    )
):
    user_dept = user_context.get("department", "Unknown")

    # СТРОГАЯ ПРОВЕРКА ABAC
    if user_dept != required_dept:
        raise HTTPException(
            status_code=403,
            detail=f"ABAC Policy Violation: Access denied for department '{user_dept}'. Required: '{required_dept}'."
        )

    if amount > max_amount:
        raise HTTPException(
            status_code=403,
            detail=f"ABAC Policy Violation: Requested amount ${amount} exceeds limit of ${max_amount}."
        )

    return {
        "status": "success",
        "message": f"Invoice {invoice_id} for ${amount} successfully approved by employee from '{user_dept}' department."
    }