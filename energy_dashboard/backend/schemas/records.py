from typing import List, Optional

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Сообщение об ошибке")


class DeleteResponse(BaseModel):
    success: bool = Field(..., description="Признак успешного удаления")
    id: Optional[int] = Field(None, description="ID удалённой записи")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Статус сервиса")

