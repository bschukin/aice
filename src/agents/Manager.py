from src.agents.BaseAgent import BaseAgent


class Manager(BaseAgent):
    def __init__(self, name: str = "Babalyan"):
        super().__init__(role="manager", name=name)

    def do_something(self):
        print("Менеджер управляет")