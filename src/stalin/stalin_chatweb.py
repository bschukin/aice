import sys
from pathlib import Path
import streamlit as st
from streamlit.components.v1 import html


# Первая команда Streamlit
st.set_page_config(layout="wide", page_title="Сталин")
# 2. Убираем отступы от HTML
st.markdown("""
<style>
.stMarkdown iframe {
    margin-top: -5rem !important;
    height: 0 !important;
}
</style>
""", unsafe_allow_html=True)
# 3. JS для скролла (добавьте это)
html("""
<script>
document.addEventListener('keydown', function(e) {
    const preview = document.querySelector('.markdown-preview');
    if (!preview) return;

    const active = document.activeElement;
    if (['INPUT','TEXTAREA','BUTTON'].includes(active.tagName)) return;

    if (e.key === 'ArrowDown') {
        preview.scrollBy({top: 50, behavior: 'smooth'});
        e.preventDefault();
    } else if (e.key === 'ArrowUp') {
        preview.scrollBy({top: -50, behavior: 'smooth'});
        e.preventDefault();
    }
});
</script>
""", height=0)

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


# Заголовок
st.title("Сталин")
from stalin.Stalin import Stalin
stalin = Stalin()

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
        # Добавляем контейнер для выравнивания
        cols = st.columns([1, 0.1])  # Первая колонка - поле ввода, вторая - кнопка

        with cols[0]:
            custom_input = st.text_area(
                "Введите запрос...",
                key="custom_chat_input",
                height=75,
                label_visibility="collapsed",
                help="Нажмите Ctrl+Enter для отправки"
            )

        with cols[1]:
            # Добавляем пустое пространство для вертикального выравнивания
            st.empty()
            submit_button = st.form_submit_button("→", type="secondary")

        # Добавляем CSS для стилизации
        st.markdown("""
        <style>
        /* Стили для формы */
        div[data-testid="stForm"] {
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 0.5rem;
            margin-top: 1rem;
            background-color: #f9fafb;
        }

        /* Стили для кнопки */
        div[data-testid="stFormSubmitButton"] button {
            min-height: 3rem;
            margin-top: 0.5rem;
        }

        /* Стили для поля ввода */
        div[data-testid="stTextArea"] textarea {
            box-shadow: none !important;
            border: none !important;
            background-color: transparent !important;
        }

        /* Убираем лишние отступы */
        div[data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)

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
            response = stalin.chat(prompt)
            stalin.dump_state()

            st.session_state.messages.append({"role": "assistant", "content": response})
            with chat_history:
                with st.chat_message("assistant"):
                    st.markdown(response)
                    st.session_state.document_text = stalin.get_HRD()

# Правая колонка - документ
with doc_col:
    st.subheader("Документ", divider="gray")

    # Инициализация текста
    if "document_text" not in st.session_state:
        st.session_state.document_text = stalin.get_HRD()

    # Создаем вкладки
    tab_edit, tab_preview = st.tabs(["Редактор", "Предпросмотр"])

    # Вкладка редактора
    with tab_edit:
        edited_text = st.text_area(
            "Редактор Markdown",
            st.session_state.document_text,
            height=450,
            label_visibility="collapsed",
            key="doc_editor"
        )

        # Сохраняем изменения
        if edited_text != st.session_state.document_text:
            st.session_state.document_text = edited_text

    # Вкладка предпросмотра

    with tab_preview:
        st.markdown("""
        <style>
        .markdown-preview {
            font-family: -apple-system, sans-serif;
            line-height: 1.35;
            color: #333;
            font-size: 14px;
            padding: 0;
        }
        /* Жесткое переопределение h1 */
        div[data-testid="stMarkdownContainer"] .markdown-preview h1 {
            font-size: 1.8rem !important;
            margin: 2.8rem 0 0.2rem 0 !important;
            line-height: 1.2 !important;
            font-weight: 600 !important;
            padding: 0 !important;
            border: none !important;
        }
        /*.markdown-preview h1::before {
            content: "— ";
            margin-right: 8px;
            color: #444;
            font-weight: bold;
        }*/
        .markdown-preview h2 {
            font-size: 1.25rem;
            margin: 0.7rem 0 0.35rem 0 !important;
            font-weight: 550;
            padding-left: 1.0rem;
        }
        /*.markdown-preview h2::before {
            content: "– ";
            margin-right: 6px;
            color: #666;
        }*/
        .markdown-preview h3 {
            font-size: 1.05rem !important;  /* Чуть больше базового */
            color: #777 !important;         /* Полноценный чёрный */
            margin: 0.6rem 0 0.3rem 0 !important;
            padding-left: 1.8rem;
            font-weight: 550 !important;    /* Полужирный */
            letter-spacing: 0.01em;        /* Чуть разряженные буквы */
        }
        /*.markdown-preview h3::before {
            content: "- ";
            margin-right: 4px;
            color: #888;
        }*/
        .markdown-preview p {
            margin: 0.4rem 0 !important;
        }
        .markdown-preview ul, ol {
            margin: 0.4rem 0 !important;
            padding-left: 2.4rem;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(
            f'<div class="markdown-preview" tabindex="0" style="height:450px; overflow:auto; padding:0.5rem;">{st.session_state.document_text}</div>',
            unsafe_allow_html=True
        )

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