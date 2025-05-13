import streamlit as st
import pdfplumber
import time
from io import BytesIO

st.set_page_config(layout="wide")
st.title("📝 OET Reading Practice")

# Таймер
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "seconds_left" not in st.session_state:
    st.session_state.seconds_left = 15 * 60

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

# Функція для відображення таймера
def display_timer():
    remaining = st.session_state.seconds_left
    mins, secs = divmod(remaining, 60)
    st.markdown(f"### ⏰ {mins:02}:{secs:02}")

# Кнопка старту таймера
if st.button("▶️ Старт 15 хвилин"):
    st.session_state.start_time = time.time()
    st.session_state.seconds_left = 15 * 60

# Оновлення таймера
if st.session_state.start_time:
    elapsed = int(time.time() - st.session_state.start_time)
    st.session_state.seconds_left = max(0, 15 * 60 - elapsed)
    display_timer()
    if st.session_state.seconds_left == 0:
        st.warning("⛔ Час вийшов!")
else:
    display_timer()
