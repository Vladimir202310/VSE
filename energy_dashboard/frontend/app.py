import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Energy Dashboard | task_04", layout="wide")
st.title("⚡ Energy Market Dashboard | task_04")

st.sidebar.title("⚙️ Управление")

# ─────────────────────────────────────────
# SESSION STATE — инициализация
# ─────────────────────────────────────────
if "upload_done" not in st.session_state:
    st.session_state["upload_done"] = False
if "uploaded_file_id" not in st.session_state:
    st.session_state["uploaded_file_id"] = None
if "upload_message" not in st.session_state:
    st.session_state["upload_message"] = None

# ─────────────────────────────────────────
# CALLBACK — срабатывает ТОЛЬКО при смене файла
# ─────────────────────────────────────────
def on_file_change():
    f = st.session_state["csv_uploader"]
    if f is None:
        return

    file_id = f"{f.name}_{f.size}"

    # Если это тот же файл — не грузим повторно
    if st.session_state["uploaded_file_id"] == file_id:
        return

    try:
        res = requests.post(
            f"{API_URL}/upload-csv",
            files={"file": (f.name, f.getvalue(), "text/csv")}
        )
        if res.status_code == 201:
            data = res.json()
            st.session_state["uploaded_file_id"] = file_id
            st.session_state["upload_done"] = True
            st.session_state["upload_message"] = ("success", f"✅ Загружено {data['rows']} строк!")
        else:
            st.session_state["upload_message"] = ("error", f"❌ {res.json().get('detail', 'Ошибка')}")
    except Exception as e:
        st.session_state["upload_message"] = ("error", f"❌ API недоступен: {e}")

# ─────────────────────────────────────────
# 1. FILE UPLOADER С CALLBACK
# ─────────────────────────────────────────
st.sidebar.subheader("📂 Выбор файла с данными")

st.sidebar.file_uploader(
    "Выберите CSV файл",
    type=["csv"],
    key="csv_uploader",
    on_change=on_file_change  # срабатывает ТОЛЬКО при смене файла!
)

# Показываем сообщение после загрузки
if st.session_state["upload_message"]:
    msg_type, msg_text = st.session_state["upload_message"]
    if msg_type == "success":
        st.sidebar.success(msg_text)
    else:
        st.sidebar.error(msg_text)

st.sidebar.divider()

# ─────────────────────────────────────────
# ЗАГРУЗКА ДАННЫХ ИЗ API
# ─────────────────────────────────────────
def fetch_data():
    try:
        res = requests.get(f"{API_URL}/records")
        if res.status_code == 200:
            return pd.DataFrame(res.json())
        return pd.DataFrame()
    except:
        return pd.DataFrame()

df = fetch_data()

# ─────────────────────────────────────────
# 2. ОКНО ПРОСМОТРА
# ─────────────────────────────────────────
if not df.empty:
    total = len(df)
    st.sidebar.subheader("🔍 Окно просмотра данных")

    window_size = st.sidebar.slider(
        "📏 Размер окна (строк)",
        min_value=10,
        max_value=total,
        value=min(100, total),
        step=10
    )
    max_offset = max(0, total - window_size)
    offset = st.sidebar.slider(
        "↔️ Смещение окна",
        min_value=0,
        max_value=max_offset,
        value=0,
        step=1
    )
    st.sidebar.caption(
        f"📊 Строки: **{offset+1}** — **{min(offset+window_size, total)}** из **{total}**"
    )
    display_df = df.iloc[offset: offset + window_size].copy()

else:
    display_df = pd.DataFrame()
    offset = 0
    window_size = 0
    total = 0

st.sidebar.divider()

# ─────────────────────────────────────────
# 3. ДОБАВЛЕНИЕ ЗАПИСИ
# ─────────────────────────────────────────
st.sidebar.subheader("➕ Добавить запись")
with st.sidebar.form("add_form"):
    new_ts    = st.text_input("Timestep", placeholder="2024-01-01 00:00")
    new_c_eur = st.number_input("Consumption EUR", min_value=0.0, step=0.1)
    new_c_sib = st.number_input("Consumption SIB", min_value=0.0, step=0.1)
    new_p_eur = st.number_input("Price EUR",        min_value=0.0, step=0.1)
    new_p_sib = st.number_input("Price SIB",        min_value=0.0, step=0.1)

    if st.form_submit_button("✅ Отправить POST"):
        if not new_ts:
            st.sidebar.error("⚠️ Укажите Timestep")
        else:
            payload = {
                "timestep": new_ts,
                "consumption_eur": float(new_c_eur),
                "consumption_sib": float(new_c_sib),
                "price_eur": float(new_p_eur),
                "price_sib": float(new_p_sib)
            }
            try:
                res = requests.post(f"{API_URL}/records", json=payload)
                if res.status_code == 201:
                    new_id = res.json().get("id")
                    st.sidebar.success(f"✅ Запись добавлена! ID: {new_id}")
                    st.rerun()
                else:
                    st.sidebar.error(f"❌ {res.json().get('detail', 'Ошибка')}")
            except Exception as e:
                st.sidebar.error(f"❌ Ошибка: {e}")

st.sidebar.divider()

# ─────────────────────────────────────────
# 4. УДАЛЕНИЕ ЗАПИСИ
# ─────────────────────────────────────────
st.sidebar.subheader("🗑️ Удалить запись")
del_id = st.sidebar.number_input("ID для удаления", min_value=1, step=1)
if st.sidebar.button("❌ Выполнить DELETE"):
    try:
        res = requests.delete(f"{API_URL}/records/{int(del_id)}")
        if res.status_code == 200:
            st.sidebar.success(f"✅ ID {del_id} удалён")
            st.rerun()
        else:
            st.sidebar.error(f"❌ {res.json().get('detail', 'ID не найден')}")
    except Exception as e:
        st.sidebar.error(f"❌ Ошибка: {e}")

# ─────────────────────────────────────────
# ОСНОВНАЯ ПАНЕЛЬ
# ─────────────────────────────────────────
if not df.empty:
    st.subheader(f"📋 Таблица — строки {offset+1}–{min(offset+window_size, total)} из {total}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.subheader("📈 Графики")
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line(
            display_df, x="timestep",
            y=["consumption_eur", "consumption_sib"],
            title="Потребление: EUR vs SIB",
            labels={"value": "Потребление", "variable": "Регион"},
            markers=False
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.line(
            display_df, x="timestep",
            y=["price_eur", "price_sib"],
            title="Цены: EUR vs SIB",
            labels={"value": "Цена", "variable": "Регион"},
            markers=False
        )
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("⚠️ Нет данных. Выберите CSV файл в сайдбаре.")
    st.info("💡 Backend: `uvicorn backend.main:app --reload --port 8000`")