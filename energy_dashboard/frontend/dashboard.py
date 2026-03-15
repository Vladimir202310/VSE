import streamlit as st
import pandas as pd
import requests
from functools import lru_cache

API_URL = "https://vse-fastapi.onrender.com/records"


@lru_cache(maxsize=1)
def load_data():
    try:
        with st.spinner("Загружаю данные из базы..."):
            resp = requests.get(API_URL, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        if not data:
            return pd.DataFrame(
                columns=[
                    "timestep",
                    "consumption_eur",
                    "consumption_sib",
                    "price_eur",
                    "price_sib",
                ]
            )
        df = pd.DataFrame(data)
        df["timestep"] = pd.to_datetime(df["timestep"])
        return df
    except requests.RequestException as e:
        st.error(f"Ошибка при загрузке данных из API: {e}")
        return pd.DataFrame(
            columns=[
                "timestep",
                "consumption_eur",
                "consumption_sib",
                "price_eur",
                "price_sib",
            ]
        )


def main():
    st.title("Панель мониторинга энергопотребления")

    # --- Блок загрузки CSV и импорта в базу ---
    st.sidebar.header("Загрузка данных из CSV")
    uploaded_file = st.sidebar.file_uploader("Выберите CSV файл", type="csv")

    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            needed_cols = {
                "timestep",
                "consumption_eur",
                "consumption_sib",
                "price_eur",
                "price_sib",
            }
            if not needed_cols.issubset(df_upload.columns):
                st.sidebar.error("В CSV нет всех необходимых колонок.")
            else:
                if st.sidebar.button("Импортировать CSV в базу"):
                    imported = 0
                    try:
                        with st.spinner("Импортирую записи в базу..."):
                            for _, row in df_upload.iterrows():
                                payload = {
                                    "timestep": pd.to_datetime(
                                        row["timestep"]
                                    ).isoformat(),
                                    "consumption_eur": float(
                                        row["consumption_eur"]
                                    ),
                                    "consumption_sib": float(
                                        row["consumption_sib"]
                                    ),
                                    "price_eur": float(row["price_eur"]),
                                    "price_sib": float(row["price_sib"]),
                                }
                                resp = requests.post(
                                    API_URL, json=payload, timeout=10
                                )
                                resp.raise_for_status()
                                imported += 1
                        st.sidebar.success(
                            f"Импортировано записей: {imported}"
                        )
                        load_data.clear()
                    except requests.RequestException as e:
                        st.sidebar.error(
                            f"Ошибка при импорте CSV: {e}"
                        )
        except Exception as e:
            st.sidebar.error(f"Не удалось прочитать CSV: {e}")

    # --- Основные данные и графики ---
    df = load_data()

    if df.empty:
        st.info("В базе пока нет данных для отображения.")
        return

    st.subheader("Сырые данные")
    st.dataframe(df.sort_values("timestep"))

    st.subheader("Графики потребления и цен")
    st.line_chart(
        df.set_index("timestep")[["consumption_eur", "consumption_sib"]]
    )
    st.line_chart(df.set_index("timestep")[["price_eur", "price_sib"]])


if __name__ == "__main__":
    main()
