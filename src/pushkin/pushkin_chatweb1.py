import sys
from pathlib import Path
import streamlit as st

# Первая команда Streamlit
st.set_page_config(layout="wide", page_title="Пушкин Первый")
st.markdown("""
<style>
.stApp {
    margin-top: -2.5rem !important;
}
header {
    height: 2rem !important;
}
h1 {
    margin-top: -1.5rem !important;
    padding-top: 0rem !important;
    font-size: 2.2rem !important;
    color: #555555 !important;
    font-weight: 500 !important;
}
/* Стили для кастомного поля ввода */
.custom-textarea {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 0.5rem;
    resize: none;
    font-family: inherit;
    font-size: inherit;
    min-height: 60px;
    max-height: 200px;
    overflow-y: auto !important;
}
.custom-textarea:focus {
    outline: none;
    border-color: #4d90fe;
    box-shadow: 0 0 0 2px rgba(77, 144, 254, 0.2);
}
.custom-container {
    padding: 0.5rem;
    position: relative;
}
.send-button {
    position: absolute;
    right: 1rem;
    bottom: 1rem;
    background: #f0f2f6;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    cursor: pointer;
    opacity: 0.7;
}
.send-button:hover {
    opacity: 1;
    background: #e0e2e6;
}
</style>
""", unsafe_allow_html=True)

# Настройка путей
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.insert(0, str(project_root))

from pushkin.Pushkin import Pushkin

# Заголовок
st.title("Пушкин Первый")

pushkin = Pushkin()

# Создаем две колонки (можно настроить соотношение)
chat_col, doc_col = st.columns([7, 9], gap="medium")

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

    # Кастомное поле ввода с многострочной поддержкой
    with st.form(key="chat_input_form", clear_on_submit=True):
        custom_input = st.text_area(
            "Введите запрос...",
            key="custom_chat_input",
            height=100,
            label_visibility="collapsed",
            help="Нажмите Ctrl+Enter для отправки"
        )
        submit_button = st.form_submit_button("Отправить")

    # Обработка отправки сообщения
    if submit_button or (st.session_state.get("ctrl_enter_pressed", False) and custom_input.strip()):
        # Сбросим флаг Ctrl+Enter
        if "ctrl_enter_pressed" in st.session_state:
            st.session_state.ctrl_enter_pressed = False

        prompt = custom_input.strip()
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_history:
                with st.chat_message("user"):
                    st.markdown(prompt)

            # Генерация ответа
            response = pushkin.chat(prompt)
            pushkin.dump_state()

            st.session_state.messages.append({"role": "assistant", "content": response})
            with chat_history:
                with st.chat_message("assistant"):
                    st.markdown(response)
                    st.session_state.document_text = pushkin.get_STD()

# Правая колонка - документ
with doc_col:
    st.subheader("Документ", divider="gray")

    # Инициализация текста
    if "document_text" not in st.session_state:
        st.session_state.document_text = pushkin.get_STD()

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
        # Создаем контейнер с фиксированной высотой и скроллбаром
        st.markdown(
            f"""
            <div style="height: 400px; overflow-y: auto; border: 1px solid #e1e4e8; border-radius: 0.25rem; padding: 0.5rem;">
            {st.session_state.document_text}
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

# JavaScript для обработки Ctrl+Enter
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.querySelector('textarea[aria-label="Введите запрос..."]');

    if (textarea) {
        textarea.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                // Установим флаг в sessionState
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    key: 'ctrl_enter_pressed',
                    value: true
                }, '*');

                // Отправим форму
                const form = textarea.closest('form');
                if (form) {
                    const submitButton = form.querySelector('button[type="submit"]');
                    if (submitButton) {
                        submitButton.click();
                    }
                }
            }
        });
    }
});
</script>
""", unsafe_allow_html=True)