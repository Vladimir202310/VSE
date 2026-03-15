import requests
import pandas as pd
import streamlit as st
from datetime import datetime


API_URL = "https://vse-fastapi.onrender.com/records"

st.set_page_config(
    page_title="Energy Dashboard",
    layout="wide",
)


@st.cache_data
def load_data():
    """Загружаем все записи из backend и готовим DataFrame."""
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data)
    if df.empty:
        return df

    df["timestep"] = pd.to_datetime(df["timestep"])
    df = df.sort_values("timestep").reset_index(drop=True)
    return df


def main():
    st.title("Панель мониторинга энергопотребления")

    # --------- Блок CRUD (добавление / удаление) ---------
    st.sidebar.header("Управление записями")

    st.sidebar.subheader("Добавить запись")
    new_date = st.sidebar.date_input("Дата", value=datetime(2006, 9, 1).date())
    new_time = st.sidebar.time_input("Время", value=datetime(2006, 9, 1, 0, 0).time())
    new_consumption_eur = st.sidebar.number_input(
        "Consumption (EUR)", min_value=0.0, step=100.0
    )
    new_consumption_sib = st.sidebar.number_input(
        "Consumption (SIB)", min_value=0.0, step=100.0
    )
    new_price_eur = st.sidebar.number_input(
        "Price (EUR)", min_value=0.0, step=1.0
    )
    new_price_sib = st.sidebar.number_input(
        "Price (SIB)", min_value=0.0, step=1.0
    )

    if st.sidebar.button("Сохранить запись"):
        ts = datetime.combine(new_date, new_time)
        payload = {
            "timestep": ts.isoformat(),
            "consumption_eur": new_consumption_eur,
            "consumption_sib": new_consumption_sib,
            "price_eur": new_price_eur,
            "price_sib": new_price_sib,
        }
        try:
            resp = requests.post(API_URL, json=payload)
            resp.raise_for_status()
            st.sidebar.success("Запись успешно добавлена.")
            load_data.clear()
        except requests.RequestException as e:
            st.sidebar.error(f"Ошибка при добавлении записи: {e}")

    st.sidebar.subheader("Удалить запись по ID")
    delete_id = st.sidebar.number_input(
        "ID для удаления", min_value=1, step=1
    )
    if st.sidebar.button("Удалить"):
        try:
            resp = requests.delete(f"{API_URL}/{int(delete_id)}")
            if resp.status_code == 200:
                st.sidebar.success(f"Запись с ID={int(delete_id)} удалена.")
                load_data.clear()
            elif resp.status_code == 404:
                st.sidebar.warning("Запись с таким ID не найдена.")
            else:
                st.sidebar.error(f"Ошибка удаления: {resp.status_code}")
        except requests.RequestException as e:
            st.sidebar.error(f"Ошибка при удалении записи: {e}")

    # --------- Загрузка данных ---------
    df = load_data()

    if df.empty:
        st.warning(
            "Данные не найдены. Убедитесь, что backend запущен и база не пустая."
        )
        return

    # --------- Оконный просмотр по времени ---------
    st.sidebar.markdown("---")
    st.sidebar.header("Просмотр данных")

    n = len(df)

    # 1. Размер окна
    window_size = st.sidebar.slider(
        "Размер окна (число точек)",
        min_value=10,
        max_value=min(10000, n),
        value=min(100, n),
        step=10,
    )

    if n <= window_size:
        start_idx = 0
        end_idx = n
        st.sidebar.write(f"Всего {n} записей, показываем все.")
    else:
        max_start = n - window_size
        start_idx = st.sidebar.slider(
            "Сдвиг окна (0 = самое старое, максимум = последние данные)",
            min_value=0,
            max_value=max_start,
            value=max_start,  # по умолчанию последнее окно
            step=1,
        )
        end_idx = start_idx + window_size

    df_window = df.iloc[start_idx:end_idx].copy()

    start_dt = df_window["timestep"].min()
    end_dt = df_window["timestep"].max()

    st.caption(
        f"Показаны данные c {start_dt.date()} по {end_dt.date()} "
        f"({len(df_window)} записей из {len(df)})"
    )

    # --------- Таблица ---------
    st.subheader("Таблица данных (окно)")
    st.dataframe(df_window, use_container_width=True)

    # --------- Графики ---------
    df_plot = df_window.set_index("timestep")

    if df_plot.empty:
        st.info("В выбранном окне нет данных для отображения.")
        return

    st.subheader("Потребление, кВт·ч")
    st.line_chart(
        df_plot[["consumption_eur", "consumption_sib"]],
        use_container_width=True,
    )

    st.subheader("Цена")
    st.line_chart(
        df_plot[["price_eur", "price_sib"]],
        use_container_width=True,
    )


if __name__ == "__main__":
    main()

