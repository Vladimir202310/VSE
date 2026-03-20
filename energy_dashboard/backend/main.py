from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, validator


class RecordBase(BaseModel):
    timestamp: datetime = Field(..., description="Временная метка")
    consumption_eu: float = Field(..., ge=0, description="Потребление энергии в европейской части")
    consumption_as: float = Field(..., ge=0, description="Потребление энергии в азиатской части")
    price_eu: float = Field(..., ge=0, description="Цена в европейской части")
    price_as: float = Field(..., ge=0, description="Цена в азиатской части")

    @validator("timestamp", pre=True)
    def parse_timestamp(cls, v):
        if isinstance(v, datetime):
            return v
        # CSV может хранить дату как строку
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                return datetime.strptime(v, fmt)
            except Exception:
                continue
        raise ValueError("Неверный формат даты")


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    id: int = Field(..., ge=0, description="Уникальный идентификатор записи")

    class Config:
        orm_mode = True


class RecordsResponse(BaseModel):
    records: List[Record]

