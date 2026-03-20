from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import pandas as pd
from pathlib import Path

from .schemas.main import RecordBase, RecordCreate, RecordRead
from .schemas.records import RecordsRepository

app = FastAPI(title="Energy Dashboard API")

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "data.csv"

repo = RecordsRepository(csv_path=DATA_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    try:
        repo.load()
    except Exception as exc:
        raise RuntimeError(f"Failed to load data: {exc}")


@app.get("/records", response_model=List[RecordRead])
def get_records():
    return repo.get_all()


@app.post("/records", response_model=RecordRead, status_code=201)
def create_record(record: RecordCreate):
    try:
        created = repo.add(record)
        repo.save()
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


@app.delete("/records/{record_id}", status_code=204)
def delete_record(record_id: int):
    try:
        repo.delete(record_id)
        repo.save()
    except KeyError:
        raise HTTPException(status_code=404, detail="Record with given id not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
    return
