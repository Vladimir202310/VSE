import os
from fastapi import FastAPI
from .routers import router as records_router  # относительный импорт

app = FastAPI()
app.include_router(records_router, prefix="/records", tags=["records"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
    )

