from pathlib import Path
from typing import List, Optional

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
CSV_PATH = DATA_DIR / "energy.csv"


class RecordsRepository:
    def __init__(self, csv_path: Path = CSV_PATH):
        self.csv_path = csv_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not self.csv_path.exists():
            # Создаём пустой CSV с правильными столбцами
            df = pd.DataFrame(
                columns=[
                    "id",
                    "time",
                    "consumption_eu",
                    "consumption_asia",
                    "price_eu",
                    "price_asia",
                ]
            )
            df.to_csv(self.csv_path, index=False)

    def _read_df(self) -> pd.DataFrame:
        df = pd.read_csv(self.csv_path)
        if "id" not in df.columns:
            raise ValueError("CSV must contain 'id' column")
        return df

    def _write_df(self, df: pd.DataFrame) -> None:
        df.to_csv(self.csv_path, index=False)

    def get_all(self) -> List[dict]:
        df = self._read_df()
        return df.to_dict(orient="records")

    def get_next_id(self) -> int:
        df = self._read_df()
        if df.empty:
            return 1
        return int(df["id"].max()) + 1

    def add_record(self, record: dict) -> dict:
        df = self._read_df()
        record_with_id = {**record, "id": self.get_next_id()}
        df = pd.concat([df, pd.DataFrame([record_with_id])], ignore_index=True)
        self._write_df(df)
        return record_with_id

    def delete_record(self, record_id: int) -> bool:
        df = self._read_df()
        before = len(df)
        df = df[df["id"] != record_id]
        after = len(df)
        if before == after:
            return False
        self._write_df(df)
        return True


