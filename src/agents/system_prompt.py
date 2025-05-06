from paths import Paths, env_var_path_prompts_default
from utils.file_io import read_project_file, read_file


class SystemPrompt():

    _project:str
    _agent:str
    _prompt:str = None

    """
    Загружает системный промпт для роли в проекте.
    Дефолтный промпт ищется по адресу src/agents/prompts/[role].prompt.md
    Далее ищется промпт по адресу data/[project]/[role].prompt.md.
    Консьюмеру отдается промпт либо проектный промпт (если есть), либо дефолтный (если нет проектного)
    """
    def __init__(self, agent_name: str, project: str):
        self._project = project
        self._agent = agent_name

    def get_agent_prompt(self)->str:
        if self._prompt  is not None:
            return self._prompt
        filename =  Paths().get_agent_prompt_file_name(self._agent)

        if Paths().project_artifact_exists(self._project, artifact=filename):
            self._prompt = read_project_file(self._project, filename)
            return self._prompt

        self._prompt = read_file(env_var_path_prompts_default, filename)
        if self._prompt is None:
            self._prompt = "Ты - сообразительный и остроумный ассистент-помощник"

        return self._prompt