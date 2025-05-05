import json
import os
from datetime import datetime
from pathlib import Path

from utils.FileUtils import get_project_path
from utils.strings import substring_after,substring_before
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage


class MessageHistory:
    """
      Отвечает за хранение истории сообщений
      todo: пока храним полную историю в чате. в будущем можно разбивать на куски
    """

    messages = []

    def __init__(self, project: str, agent_name: str):
        self.project = project
        self.project_dir = get_project_path(project)
        self.agent_role = agent_name
        self.filename = self.__get_history_file_name()

    def add_message(self, role, content):
        """Добавляет сообщение с автоматической датой и временем"""
        text = substring_before(content, "(@")
        model = substring_after(content, "(@")
        message = {
            'role': role,
            'content': text,
            'timestamp': datetime.now().isoformat(),  # ISO-формат даты-времени
        }

        if model!= '':
            message['model'] = model[0:-1]

        self.messages.append(message)

    def get_full_messages(self) -> list[dict]:
        """Возвращает полные сообщения со всеми метаданными"""
        return self.messages.copy()

    def get_prepared_messages(self) -> list[dict]:
        """Возвращает сообщения в формате для LLM (без служебных полей)"""
        return [
            {
                'role': msg['role'],
                'content': msg['content']
            }
            for msg in self.messages
        ]

    def get_prepared_messages_lang_chain(self) -> list[BaseMessage]:
        """Возвращает сообщения в формате для LLM (без служебных полей)"""
        langchain_messages = []
        for msg in self.messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
            elif msg["role"] == "system":
                langchain_messages.append(SystemMessage(content=msg["content"]))
        return langchain_messages

    def dump_to_file(self):
        with open(self.filename, 'w',  encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=1)


    def load_from_file(self):
        if not Path(self.filename).exists():
            return
        with open(self.filename) as f:
            self.messages = json.load(f)

    def delete_all_history(self):
        self.messages = []
        if not Path(self.filename).exists():
            return
        os.remove(self.filename)

    def __get_history_file_name(self):
        return self.project_dir / (self.agent_role + ".chat.history.json")