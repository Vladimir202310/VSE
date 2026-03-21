from pathlib import Path
from typing import List

import pandas as pd

from backend.schemas.records import RecordCreate, RecordRead

DATA_PATH = Path("data/energy.csv")
COLUMNS = ["id", "time", "consumption_eu", "consumption_as", "price_eu", "price_as"]


def _load_df() -> pd.DataFrame:
    if not DATA_PATH.exists():
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_PATH, index=False)
        return df
    df = pd.read_csv(DATA_PATH)
    return df


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
            time=row["time"],
            consumption_eu=row["consumption_eu"],
            consumption_as=row["consumption_as"],
            price_eu=row["price_eu"],
            price_as=row["price_as"],
        )
        for _, row in df.iterrows()
    ]
    return records


def add_record(data: RecordCreate) -> RecordRead:
    df = _load_df()
    new_id = 1 if df.empty else int(df["id"].max()) + 1
    new_row = {
        "id": new_id,
        "time": data.time,
        "consumption_eu": data.consumption_eu,
        "consumption_as": data.consumption_as,
        "price_eu": data.price_eu,
        "price_as": data.price_as,
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
