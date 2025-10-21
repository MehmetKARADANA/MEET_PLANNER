from fastapi import FastAPI
from app.api import employee_router,department_router,meeting_router
from app.middleware.error_handler import error_handler
app = FastAPI(title="Employee Management API")


app.middleware("http")(error_handler)
app.include_router(employee_router.router)
app.include_router(department_router.router)
app.include_router(meeting_router.router)
