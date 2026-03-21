from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class RecordBase(BaseModel):
    time: datetime = Field(..., description="Время измерения")
    consumption_eu: float = Field(..., ge=0)
    consumption_as: float = Field(..., ge=0)
    price_eu: float = Field(..., ge=0)
    price_as: float = Field(..., ge=0)

class RecordCreate(RecordBase):
    pass

class RecordRead(RecordBase):
    id: int = Field(..., ge=0)

    class Config:
        from_attributes = True  # аналог orm_mode для pydantic v2

class RecordsList(BaseModel):
    items: List[RecordRead]
