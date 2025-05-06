from src.agents.baseagent import BaseAgent


class Manager(BaseAgent):
    def __init__(self, name: str = "Babalyan", project:str='default'):
        super().__init__(role="manager", name=name, project=project)