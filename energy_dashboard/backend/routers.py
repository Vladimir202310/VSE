from fastapi import APIRouter, HTTPException, status

from .main import Record, RecordCreate, RecordsResponse
from .records import ErrorResponse, DeleteResponse
from ..repository.storage import (
    get_all_records,
    add_record,
    delete_record_by_id,
    RecordNotFoundError,
)

router = APIRouter(prefix="/records", tags=["records"])


@router.get(
    "",
    response_model=RecordsResponse,
    responses={500: {"model": ErrorResponse}},
)
def read_records():
    try:
        records = get_all_records()
        return RecordsResponse(records=records)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при чтении данных: {exc}",
        )


@router.post(
    "",
    response_model=Record,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def create_record(record: RecordCreate):
    try:
        new_record = add_record(record)
        return new_record
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при добавлении записи: {exc}",
        )


@router.delete(
    "/{record_id}",
    response_model=DeleteResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def delete_record(record_id: int):
    try:
        delete_record_by_id(record_id)
        return DeleteResponse(success=True, id=record_id)
    except RecordNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении записи: {exc}",
        )
