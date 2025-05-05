from abc import ABC, abstractmethod
from llm.llm_gate import LlmGate
from llm.message_history import MessageHistory


class BaseAgent(ABC):
    __gate = LlmGate()

    def __init__(self, role: str, name: str, project:str='default'):
        self._role = role  # Защищенное поле (по соглашению)
        self._name = name
        self._project = project
        self._history = MessageHistory(project, role)
        self._history.load_from_file()

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

    def chat(self, prompt:str, temperature = 0.0)->str:

        resp =  self.__gate.prompt(prompt, self._history.get_prepared_messages(), temperature)
        self._history.add_message("user", prompt)
        self._history.add_message("assistant", resp)
        return resp
