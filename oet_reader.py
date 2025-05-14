import streamlit as st
import pdfplumber
import time
from io import BytesIO
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")
st.title("📝 OET Reading Practice")

# Автооновлення кожну секунду (якщо таймер працює)
if "timer_running" in st.session_state and st.session_state.timer_running:
    st_autorefresh(interval=1000, key="auto_refresh")

# Ініціалізація таймера та станів
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "seconds_left" not in st.session_state:
    st.session_state.seconds_left = 15 * 60
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "user_answers" not in st.session_state:
    st.session_state.user_answers = ""

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Текст")
    text_pdf = st.file_uploader("Завантаж PDF з текстом", type="pdf", key="text")
    if text_pdf:
        with pdfplumber.open(BytesIO(text_pdf.read())) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        st.text_area("Текст", value=text, height=500, key="text_display")

with col2:
    st.subheader("❓ Питання + Відповіді")
    question_pdf = st.file_uploader("Завантаж PDF з питаннями", type="pdf", key="questions")
    if question_pdf and not st.session_state.user_answers:
        with pdfplumber.open(BytesIO(question_pdf.read())) as pdf:
            st.session_state.user_answers = "\n".join(
                page.extract_text() for page in pdf.pages if page.extract_text()
            )
    st.session_state.user_answers = st.text_area("Пиши відповіді тут:", value=st.session_state.user_answers, height=500)

# Кнопка старту таймера
if st.button("▶️ Старт 15 хвилин"):
    st.session_state.start_time = time.time()
    st.session_state.timer_running = True
    st.session_state.seconds_left = 15 * 60

# Вивід таймера
placeholder = st.empty()
if st.session_state.timer_running and st.session_state.start_time:
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 15 * 60 - elapsed)
    st.session_state.seconds_left = remaining
    if remaining == 0:
        st.session_state.timer_running = False

mins, secs = divmod(st.session_state.seconds_left, 60)
with placeholder.container():
    st.markdown(f"### ⏰ {mins:02}:{secs:02}")
    if st.session_state.seconds_left == 0:
        st.warning("⛔ Час вийшов!")

