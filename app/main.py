from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from app.api import employee_router,department_router,meeting_router,auth_router
from app.core.error_handler import error_handler
from fastapi.exceptions import RequestValidationError


app = FastAPI(title="Employee Management API")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = await request.body()
    print(f"422 Validation Error: {exc.errors()} | Body: {body.decode('utf-8')}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": body.decode("utf-8")
        }
    )

app.middleware("http")(error_handler)
app.include_router(auth_router.router)
app.include_router(employee_router.router)
app.include_router(department_router.router)
app.include_router(meeting_router.router)
