from src.agents.BaseAgent import BaseAgent


class Architect(BaseAgent):

    def __init__(self, name: str = "Vikulin"):
        super().__init__(role="architect", name=name)