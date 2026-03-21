from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import os
import uvicorn
import io
from typing import List

app = FastAPI(title="Energy Market API", version="1.0.0")

current_db_path = os.path.join(os.path.dirname(__file__), "data.csv")

class EnergyRecord(BaseModel):
    timestep: str
    consumption_eur: float
    consumption_sib: float
    price_eur: float
    price_sib: float

class EnergyRecordFull(EnergyRecord):
    id: int

def get_df():
    if not os.path.exists(current_db_path):
        df = pd.DataFrame(columns=["id","timestep","consumption_eur","consumption_sib","price_eur","price_sib"])
        df.to_csv(current_db_path, index=False)
        return df
    return pd.read_csv(current_db_path)

def get_next_id(df):
    """Следующий ID = макс + 1, либо 1 если пусто"""
    if df.empty or "id" not in df.columns:
        return 1
    return int(df["id"].max()) + 1

@app.get("/")
def root():
    return {"message": "Energy Market API", "version": "1.0.0"}

@app.get("/records", response_model=List[EnergyRecordFull])
def read_records():
    df = get_df()
    return df.to_dict(orient="records")

@app.post("/records", status_code=201)
def create_record(record: EnergyRecord):
    """Добавляет запись в конец, ID присваивается автоматически"""
    df = get_df()
    new_id = get_next_id(df)
    new_row = {"id": new_id, **record.model_dump()}
    new_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    new_df.to_csv(current_db_path, index=False)
    return {"message": "Record added", "id": new_id}

@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    """Удаляет запись по ID, ID остальных не меняются"""
    df = get_df()
    if record_id not in df['id'].values:
        raise HTTPException(status_code=404, detail="ID не найден")
    df = df[df['id'] != record_id]
    # Сохраняем без переиндексации — ID не меняем!
    df.to_csv(current_db_path, index=False)
    return {"message": f"Record {record_id} deleted"}

@app.post("/upload-csv", status_code=201)
async def upload_csv(file: UploadFile = File(...)):
    """Загружает весь CSV файл за один запрос"""
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        if "id" not in df.columns:
            df.insert(0, "id", range(1, len(df) + 1))
        df.to_csv(current_db_path, index=False)
        return {
            "message": f"Загружено {len(df)} строк",
            "columns": list(df.columns),
            "rows": len(df)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка чтения файла: {e}")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)