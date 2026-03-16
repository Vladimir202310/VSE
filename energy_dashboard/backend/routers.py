from fastapi import APIRouter, HTTPException, status
from typing import List

from schemas import RecordCreate, RecordRead  # было: from backend.schemas
from .repository.records import (  # было: from backend.repository
    get_all_records,
    add_record,
    delete_record,
)


router = APIRouter()
# дальше ручки...


@router.get("/", response_model=List[RecordRead])
def list_records():
    return get_all_records()

@router.post("/", response_model=RecordRead, status_code=status.HTTP_201_CREATED)
def create_record(record: RecordCreate):
    try:
        return add_record(record)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save record")

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_record(record_id: int):
    try:
        delete_record(record_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Record not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete record")

@router.post("/bulk", status_code=status.HTTP_201_CREATED)
def bulk_import(records: List[RecordCreate]):
    try:
        for record in records:
            add_record(record)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to bulk import records")
    return {"detail": f"Imported {len(records)} records"}

