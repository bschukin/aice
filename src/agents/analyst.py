from src.agents.baseagent import BaseAgent


class Analyst(BaseAgent):

    def __init__(self, name: str = "Levin", project:str='default'):
        super().__init__(role="analyst", name=name, project=project)