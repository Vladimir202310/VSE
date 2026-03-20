from typing import List

from fastapi import APIRouter, HTTPException, status

from .main import Record, RecordCreate
from ..repository.records import RecordsRepository

router = APIRouter(prefix="/records", tags=["records"])
repo = RecordsRepository()


@router.get("/", response_model=List[Record])
def get_records():
    try:
        raw = repo.get_all()
        return raw
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load records: {e}",
        )


@router.post("/", response_model=Record, status_code=status.HTTP_201_CREATED)
def create_record(record: RecordCreate):
    try:
        # Pydantic уже провалидировал данные
        rec_dict = record.dict()
        created = repo.add_record(
            {
                "time": rec_dict["time"].isoformat(),
                "consumption_eu": rec_dict["consumption_eu"],
                "consumption_asia": rec_dict["consumption_asia"],
                "price_eu": rec_dict["price_eu"],
                "price_asia": rec_dict["price_asia"],
            }
        )
        return created
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create record: {e}",
        )


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int):
    try:
        ok = repo.delete_record(record_id)
        if not ok:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Record with id={record_id} not found",
            )
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete record: {e}",
        )
