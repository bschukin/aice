from paths import Paths, env_var_path_prompts_default
from utils.file_io import read_project_file, read_file
from utils.md import insert_section_into_markdown, print_markdown

from loguru import logger

class SystemPrompt:

    """
    Готовится системный промпт для роли в проекте.
    1. Поиск основного промпта роли
    Дефолтный промпт ищется по адресу src/agents/prompts/[role].prompt.md
    Далее ищется промпт по адресу data/[project]/[role].prompt.md.
    Консьюмеру отдается промпт либо проектный промпт (если есть), либо дефолтный (если нет проектного).
    
    2. В основной промпт роли также добавляется командный промпт ("## О вашей команде") 
    3. Отдельный промпт о ведении документа PRD
    """
    def __init__(self, agent_name: str, project: str):
        self._project = project
        self._agent = agent_name

        self.agent_prompt = self.__get_agent_prompt()
        self.prd_schema = (SystemPrompt.load_statement_file(project, "PRD_schema.py")
                           + "\r\n" + SystemPrompt.load_statement_file(project, "PRD.example.json"))
        self.response_schema = (SystemPrompt.load_statement_file(project, "commands_schema.py")
                            + "\r\n" + SystemPrompt.load_statement_file(project, "commands.example01.md")
                            + "\r\n" + SystemPrompt.load_statement_file(project, "commands.example01.json"))


    def __get_agent_prompt(self)->str:

        #загружаем основной промпт
        prompt = self.load_prompt(self._project, self._agent)

        # загружаем  промпт команды
        team_prompt  = self.load_prompt(self._project, "team", False)
        prompt = insert_section_into_markdown(prompt, "## О вашей команде", team_prompt, delete_target_header=True)

        return prompt


    @staticmethod
    def load_prompt(project, prompt_name, use_default_prompt=True)->str:
        filename = Paths().get_agent_prompt_file_name(prompt_name)

        prompt = SystemPrompt.load_statement_file(project, filename)

        if prompt is None and use_default_prompt:
            prompt = "Ты - сообразительный и остроумный ассистент-помощник"

        return prompt

    @staticmethod
    def load_statement_file(project, filename) -> str:

        if Paths().project_artifact_exists(project, artifact=filename):
            prompt = read_project_file(project, filename)
            used_prompt = str(Paths().get_project_artifact(project, artifact=filename))
            logger.info(f"project [{project}], statement file [{filename}]. using path to load: {used_prompt} ")
            return prompt

        prompt = read_file(env_var_path_prompts_default, filename)
        used_prompt = env_var_path_prompts_default + "." + filename
        logger.info(f"project [{project}], statement file [{filename}]. using path to load: {used_prompt} ")

        return prompt