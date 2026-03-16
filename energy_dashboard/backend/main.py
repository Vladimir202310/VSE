from fastapi import FastAPI
from .routers import router as records_router  # было: from backend.routers

app = FastAPI()
app.include_router(records_router, prefix="/records", tags=["records"])




