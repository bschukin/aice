from abc import ABC, abstractmethod
from llm.LlmGate import LlmGate


class BaseAgent(ABC):
    __gate = LlmGate()

    def __init__(self, role: str, name: str):
        self._role = role  # Защищенное поле (по соглашению)
        self._name = name

    @property
    def role(self) -> str:
        """Метод для получения роли"""
        return self._role

    @property
    def name(self) -> str:
        """Метод для получения имени"""
        return self._name

    @abstractmethod
    def do_something(self):
        """Абстрактный метод, который должен быть реализован в дочерних классах"""
        pass

    def chat(cls, prompt:str, temperature = 0.0)->str:
        return cls.__gate.prompt(prompt, temperature)
