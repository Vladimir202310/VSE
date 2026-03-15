# energy_dashboard/backend/main.py

from fastapi import FastAPI
from .routers import router as records_router  # ОБРАТИ ВНИМАНИЕ: точка перед routers

app = FastAPI()

app.include_router(records_router, prefix="/records", tags=["records"])

