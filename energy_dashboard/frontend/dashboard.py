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

    # --- Добавление одной записи вручную ---
    st.sidebar.header("Добавить запись вручную")
    with st.sidebar.form("add_record_form"):
        ts = st.text_input("timestep (ISO 8601)", "")
        cons_eur = st.number_input("consumption_eur", value=0.0)
        cons_sib = st.number_input("consumption_sib", value=0.0)
        price_eur = st.number_input("price_eur", value=0.0)
        price_sib = st.number_input("price_sib", value=0.0)
        submitted_add = st.form_submit_button("Добавить запись")

    if submitted_add:
        try:
            payload = {
                "timestep": pd.to_datetime(ts).isoformat(),
                "consumption_eur": float(cons_eur),
                "consumption_sib": float(cons_sib),
                "price_eur": float(price_eur),
                "price_sib": float(price_sib),
            }
            with st.spinner("Отправляю запись в базу..."):
                resp = requests.post(API_URL, json=payload, timeout=10)
                resp.raise_for_status()
            st.sidebar.success("Запись добавлена")
            load_data.clear()
        except Exception as e:
            st.sidebar.error(f"Не удалось добавить запись: {e}")

    # --- Удаление записи по ID ---
    st.sidebar.header("Удалить запись по ID")
    del_id = st.sidebar.text_input("ID записи для удаления", "")
    if st.sidebar.button("Удалить запись"):
        if not del_id:
            st.sidebar.error("Укажите ID записи.")
        else:
            try:
                with st.spinner("Удаляю запись..."):
                    resp = requests.delete(
                        f"{API_URL}/{del_id}", timeout=10
                    )
                    resp.raise_for_status()
                st.sidebar.success("Запись удалена")
                load_data.clear()
            except requests.RequestException as e:
                st.sidebar.error(f"Не удалось удалить запись: {e}")

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
