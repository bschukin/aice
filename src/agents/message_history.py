import json
import os
from datetime import datetime

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from paths import Paths
from utils.sugar import get_last_elements


class MessageHistory:
    """
      Отвечает за хранение истории сообщений.
      todo: пока храним полную историю в чате. в будущем можно разбивать на куски
    """

    def __init__(self, project: str, agent_name: str):
        self.project = project
        self.agent = agent_name
        self.history_file = Paths().get_agent_history_file(self.project, self.agent)
        self.messages = self.__load_from_file()

    def add_message(self, role, content, tech_content:str = None, model:str = None, error:bool = False):

        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
        if error:
            message['error'] = True

        if tech_content:
            message['tech_content'] = tech_content

        if model:
            message['model'] = model

        self.messages.append(message)

    def get_length(self) -> int:
        return len(self.messages)

    def get_full_messages(self, max_length: int | None = None) -> list[dict]:
        """Возвращает полные сообщения со всеми метаданными и контентом"""
        return get_last_elements(self.messages.copy(), max_length)


    def get_prepared_messages(self, max_length: int | None = None) -> list[dict]:
        """Возвращает сообщения в формате для LLM (без служебных полей)"""
        list =  [
            {
                'role': msg['role'],
                'content': msg['content']
            }
            for msg in self.messages
        ]
        return get_last_elements(list, max_length)

    def get_prepared_messages_lang_chain(self, max_length: int | None = None) -> list[BaseMessage]:
        """Возвращает сообщения в формате для LLM (без служебных полей)"""
        langchain_messages = []
        for msg in self.messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
            elif msg["role"] == "system":
                langchain_messages.append(SystemMessage(content=msg["content"]))
        return get_last_elements(langchain_messages, max_length)

    def dump_to_file(self):
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, 'w',  encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=1)

    def __load_from_file(self)->[]:
        if not self.history_file.exists():
            return []
        with open(self.history_file) as f:
            return json.load(f)

    def delete_all_history(self):
        self.messages = []
        if not self.history_file.exists():
            return
        os.remove(self.history_file)
