from src.agents.baseagent import BaseAgent


class Analyst(BaseAgent):

    def __init__(self, name: str = "Levin", project:str='default'):
        super().__init__(role="analyst", name=name, project=project)

    def _get_system_prompt(self) -> list[dict[str, str]]:
        nsb = """
                **ВАЖНО: 
                    Ответ дается только в формате JSON! (pydantic класс AgentResponse). 
                """

        agent_prompt = {'role': 'system', 'content': self._prompt.agent_prompt}
        prd_schema = {'role': 'system', 'content': self._prompt.prd_schema}
        resp_language = {'role': 'system', 'content': self._prompt.response_schema}
        nb = {'role': 'system', 'content': nsb}

        return [agent_prompt, prd_schema, resp_language, nb]