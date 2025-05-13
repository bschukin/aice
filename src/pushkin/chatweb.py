import sys
from pathlib import Path
import streamlit as st

# Первая команда Streamlit
st.set_page_config(layout="wide",  page_title="Пушкин Первый")
st.markdown("""
<style>
h1 {
    margin-top: 0px !important;
    padding-top: 0px !important;
}
</style>
""", unsafe_allow_html=True)

# Настройка путей
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.insert(0, str(project_root))
#st.warning(f"DEBUG MODE. Added to path: {project_root}")

from pushkin.Pushkin import Pushkin

# Заголовок
st.title("Пушкин Первый")

pushkin = Pushkin()

# Создаем две колонки (можно настроить соотношение)
chat_col, doc_col = st.columns([4, 4], gap="medium")

st.markdown("""
<style>
h3 {
    font-size: 18px !important;  color: #808080 !important; 
}
</style>
""", unsafe_allow_html=True)

# Левая колонка - чат
with chat_col:
    st.subheader("Чат", divider="gray")

    # Контейнер истории чата с уменьшенной высотой
    chat_history = st.container(height=400, border=False)

    # Инициализация истории
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Отображение истории
    with chat_history:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Поле ввода
    if prompt := st.chat_input("Введите запрос..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_history:
            with st.chat_message("user"):
                st.markdown(prompt)

        # Генерация ответа
        response = pushkin.chat(prompt)
#        resp_parsed = pushkin.parse_agent_response(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        with chat_history:
            with st.chat_message("assistant"):
                st.markdown(response)

# Правая колонка - документ
with doc_col:
    st.subheader("Документ", divider="gray")

    # Инициализация текста
    if "document_text" not in st.session_state:
        st.session_state.document_text = (
            "## Заголовок\n\n"
            "Это **жирный текст** и *курсив*.\n\n"
            "```python\nprint('Hello, World!')\n```\n\n"
            "- Список\n- Элементы"
        )

    # Создаем вкладки
    tab_edit, tab_preview = st.tabs(["Редактор", "Предпросмотр"])

    # Вкладка редактора
    with tab_edit:
        edited_text = st.text_area(
            "Редактор Markdown",
            st.session_state.document_text,
            height=400,
            label_visibility="collapsed",
            key="doc_editor"
        )

        # Сохраняем изменения
        if edited_text != st.session_state.document_text:
            st.session_state.document_text = edited_text

    # Вкладка предпросмотра
    with tab_preview:
        st.markdown("**Результат:**")
        st.markdown(st.session_state.document_text)  # Рендеринг Markdown