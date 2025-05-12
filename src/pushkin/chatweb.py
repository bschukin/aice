import sys
from pathlib import Path

# Добавляем корень проекта в Python path
project_root = Path(__file__).parent.parent.parent  # Путь к папке `aice`
sys.path.append(str(project_root))


import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))
st.warning(f"DEBUG MODE. Added to path: {project_root}")

from pushkin.Pushkin import Pushkin

# Минимальная настройка
#st.set_page_config(page_title="Пушкин 1")

# Заголовок
st.title("Пушкин Первый")

pushkin = Pushkin()

# История чата
if "messages" not in st.session_state:
    st.session_state.messages = []

# Показ истории
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле ввода (стандартное)
if prompt := st.chat_input("Введите запрос..."):
    # Сохраняем вопрос
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Генерируем ответ
    response = pushkin.chat(prompt)
    resp_parsed=pushkin.parse_agent_response(response)
    # Показываем ответ
    st.session_state.messages.append({"role": "assistant", "content": resp_parsed})
    with st.chat_message("assistant"):
        st.markdown(resp_parsed)