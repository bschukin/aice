from abc import ABC

from agents.system_prompt import SystemPrompt
from llm.llm_gate import LlmGate
from agents.message_history import MessageHistory


class BaseAgent(ABC):
    __gate = LlmGate()

    def __init__(self, role: str, name: str, project: str = 'default'):
        self._role = role  # Защищенное поле (по соглашению)
        self._name = name
        self._project = project
        self._prompt = SystemPrompt(role, project)
        self._history = MessageHistory(project, role)

    @property
    def role(self) -> str:
        """Метод для получения роли"""
        return self._role

    @property
    def name(self) -> str:
        """Метод для получения имени"""
        return self._name

    def dump_state(self):
        self._history.dump_to_file()

    def reset_state(self):
        self._history.delete_all_history()

    def chat(self, prompt: str, temperature=0.0) -> str:
        messages = ([{'role': 'system', 'content': self._prompt.get_agent_prompt()}]
                    + self._history.get_prepared_messages()
                    + [{'role': 'user', 'content': prompt}])

        resp = self.__gate.request(messages, temperature)
        self._history.add_message("user", prompt)
        self._history.add_message("assistant", resp)
        return resp
