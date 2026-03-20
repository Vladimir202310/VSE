from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class RecordBase(BaseModel):
    time: datetime = Field(..., description="Время измерения")
    consumption_eu: float = Field(..., ge=0)
    consumption_asia: float = Field(..., ge=0)
    price_eu: float = Field(..., ge=0)
    price_asia: float = Field(..., ge=0)

    @validator("time", pre=True)
    def parse_time(cls, v):
        # допускаем строку из CSV
        if isinstance(v, str):
            return datetime.fromisoformat(v)
        return v


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    id: int

    class Config:
        orm_mode = True
