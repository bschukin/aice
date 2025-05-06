from src.agents.baseagent import BaseAgent


class Architect(BaseAgent):

    def __init__(self, name: str = "Vikulin", project:str='default'):
        super().__init__(role="architect", name=name, project=project)