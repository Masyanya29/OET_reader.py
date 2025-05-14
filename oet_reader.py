import streamlit as st
import pdfplumber
import time
from io import BytesIO

st.set_page_config(layout="wide")
st.title("📝 OET Reading Practice")

# Ініціалізація таймера
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "seconds_left" not in st.session_state:
    st.session_state.seconds_left = 15 * 60
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Текст")
    text_pdf = st.file_uploader("Завантаж PDF з текстом", type="pdf", key="text")
    if text_pdf:
        with pdfplumber.open(BytesIO(text_pdf.read())) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        st.text_area("Текст", value=text, height=500)

with col2:
    st.subheader("❓ Питання")
    question_pdf = st.file_uploader("Завантаж PDF з питаннями", type="pdf", key="questions")
    if question_pdf:
        with pdfplumber.open(BytesIO(question_pdf.read())) as pdf:
            questions = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        st.text_area("Питання", value=questions, height=500)

# Кнопка старту таймера
if st.button("▶️ Старт 15 хвилин"):
    st.session_state.start_time = time.time()
    st.session_state.timer_running = True
    st.session_state.seconds_left = 15 * 60

# Вивід таймера з live-оновленням
placeholder = st.empty()

if st.session_state.timer_running:
    while st.session_state.seconds_left > 0:
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, 15 * 60 - elapsed)
        st.session_state.seconds_left = remaining
        mins, secs = divmod(remaining, 60)

        with placeholder.container():
            st.markdown(f"### ⏰ {mins:02}:{secs:02}")
            time.sleep(1)
            st.experimental_rerun()
else:
    mins, secs = divmod(st.session_state.seconds_left, 60)
    with placeholder.container():
        st.markdown(f"### ⏰ {mins:02}:{secs:02}")
        if st.session_state.seconds_left == 0:
            st.warning("⛔ Час вийшов!")
