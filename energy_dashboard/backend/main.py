from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ---------- Настройки БД ----------

SQLALCHEMY_DATABASE_URL = "sqlite:///./energy.db"  # если у тебя другой путь/БД — подставь свой

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # для sqlite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ---------- SQLAlchemy-модель ----------

class EnergyRecord(Base):
    __tablename__ = "energy_records"

    id = Column(Integer, primary_key=True, index=True)
    timestep = Column(DateTime, index=True)          # из столбца timestep
    consumption_eur = Column(Float)                  # из consumption_eur
    consumption_sib = Column(Float)                  # из consumption_sib
    price_eur = Column(Float)                        # из price_eur
    price_sib = Column(Float)                        # из price_sib


# ---------- Pydantic-схемы ----------

class EnergyRecordBase(BaseModel):
    timestep: datetime
    consumption_eur: float
    consumption_sib: float
    price_eur: float
    price_sib: float


class EnergyRecordCreate(EnergyRecordBase):
    pass


class EnergyRecordRead(EnergyRecordBase):
    id: int

    class Config:
        from_attributes = True  # важно для работы с ORM [web:243][web:272]


# ---------- Инициализация БД ----------

def init_db():
    Base.metadata.create_all(bind=engine)


# ---------- Зависимость для сессии БД ----------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Приложение FastAPI ----------

app = FastAPI()

init_db()


# ---------- Эндпоинты ----------

@app.get("/records", response_model=List[EnergyRecordRead])
def read_records(db: Session = Depends(get_db)):
    records = db.query(EnergyRecord).all()
    return records



@app.get("/records/{record_id}", response_model=EnergyRecordRead)
def read_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(EnergyRecord).filter(EnergyRecord.id == record_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@app.post("/records", response_model=EnergyRecordRead)
def create_record(record: EnergyRecordCreate, db: Session = Depends(get_db)):
    db_record = EnergyRecord(
        timestep=record.timestep,
        consumption_eur=record.consumption_eur,
        consumption_sib=record.consumption_sib,
        price_eur=record.price_eur,
        price_sib=record.price_sib,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
