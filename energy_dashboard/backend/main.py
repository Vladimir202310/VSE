from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
import logging

from backend.schemas.records import RecordCreate, RecordRead
from backend.repository.records import get_all_records, add_record, delete_record

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[RecordRead])
def list_records():
    records = get_all_records()
    if records is None:
        return []
    return records


@router.post("/", response_model=RecordRead, status_code=status.HTTP_201_CREATED)
def create_record(record: RecordCreate):
    try:
        return add_record(record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in create_record: {e}")
        raise HTTPException(status_code=500, detail="Failed to save record")


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_record(record_id: int):
    try:
        delete_record(record_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Record not found")
    except Exception as e:
        logger.error(f"Error deleting record {record_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete record")


@router.post("/bulk", response_model=Dict, status_code=status.HTTP_201_CREATED)
def bulk_import(records: List[RecordCreate]) -> Dict:
    try:
        added_count = 0
        for record in records:
            add_record(record)
            added_count += 1
        return {"detail": f"Imported {added_count} records"}
    except Exception as e:
        logger.error(f"Bulk import failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to bulk import records")
