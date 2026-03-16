from pathlib import Path
from typing import List
import pandas as pd

from ..schemas.records import RecordCreate, RecordRead

DATA_PATH = Path("data/energy.csv")
COLUMNS = [
    "id",
    "timestep",
    "consumption_eur",
    "consumption_sib",
    "price_eur",
    "price_sib",
]


def _load_df() -> pd.DataFrame:
    if not DATA_PATH.exists():
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_PATH, index=False)
        return df
    df = pd.read_csv(DATA_PATH)
    # На всякий случай гарантируем наличие всех колонок
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    return df[COLUMNS]


def _save_df(df: pd.DataFrame) -> None:
    df.to_csv(DATA_PATH, index=False)


def get_all_records() -> List[RecordRead]:
    df = _load_df()
    if df.empty:
        return []
    if "id" in df.columns:
        df["id"] = df["id"].astype(int)

    records = [
        RecordRead(
            id=int(row["id"]),
            timestep=row["timestep"],
            consumption_eur=row["consumption_eur"],
            consumption_sib=row["consumption_sib"],
            price_eur=row["price_eur"],
            price_sib=row["price_sib"],
        )
        for _, row in df.iterrows()
    ]
    return records


def add_record(data: RecordCreate) -> RecordRead:
    df = _load_df()
    new_id = 1 if df.empty else int(df["id"].max()) + 1

    new_row = {
        "id": new_id,
        "timestep": data.timestep,
        "consumption_eur": data.consumption_eur,
        "consumption_sib": data.consumption_sib,
        "price_eur": data.price_eur,
        "price_sib": data.price_sib,
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    _save_df(df)
    return RecordRead(**new_row)


def delete_record(record_id: int) -> None:
    df = _load_df()
    if df.empty:
        raise KeyError("Record not found")
    mask = df["id"] != record_id
    if mask.all():
        raise KeyError("Record not found")
    df = df[mask]
    _save_df(df)

