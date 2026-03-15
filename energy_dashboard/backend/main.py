from fastapi import FastAPI
from backend.routers import router as records_router

app = FastAPI()
app.include_router(records_router, prefix="/records", tags=["records"])
