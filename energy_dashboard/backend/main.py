from fastapi import FastAPI
from energy_dashboard.backend.routers import router as records_router  # ВАЖНО: полный путь

app = FastAPI()
app.include_router(records_router, prefix="/records", tags=["records"])



