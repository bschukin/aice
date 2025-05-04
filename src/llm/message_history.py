import json
import os
from datetime import datetime

from utils.FileUtils import get_project_path


class MessageHistory:
    """
      Отвечает за хранение истории сообщений
    """

    messages = []

    def __init__(self, project: str, agent_name: str):
        self.project = project
        self.project_dir = get_project_path(project)
        self.agent_name = agent_name
        self.filename = self.__get_history_file_name()

    def add_message(self, role, content):
        """Добавляет сообщение с автоматической датой и временем"""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),  # ISO-формат даты-времени
        }
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

    def dump_to_file(self):
        with open(self.filename, 'w') as f:
            json.dump(self.messages, f, indent=1)


    def load_from_file(self):
        with open(self.filename) as f:
            self.messages = json.load(f)

    def delete_all_history(self):
        self.messages = []
        os.remove(self.filename)

    def __get_history_file_name(self):
        return self.project_dir / (self.agent_name + ".chat.history.json")