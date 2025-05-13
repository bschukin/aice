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
    def __init__(self, agent_name: str, project: str, prompt_dir:str=None):
        self._project = project
        self._agent = agent_name
        self._prompt_dir = prompt_dir

        self.agent_prompt = self.__get_agent_prompt()
        self.prd_schema = (SystemPrompt.load_statement_file(project, "PRD_schema.py")
                           + "\r\n" + SystemPrompt.load_statement_file(project, "PRD.example.json"))
        self.response_schema = (SystemPrompt.load_statement_file(project, "commands_schema.py")
                            + "\r\n" + SystemPrompt.load_statement_file(project, "commands.example01.md")
                            + "\r\n" + SystemPrompt.load_statement_file(project, "commands.example01.json"))


    def __get_agent_prompt(self)->str:

        #загружаем основной промпт
        prompt = self.load_prompt(self._project, self._agent, prompt_dir=self._prompt_dir)

        # загружаем  промпт команды
        team_prompt  = self.load_prompt(self._project, "team", False)
        prompt = insert_section_into_markdown(prompt, "## О вашей команде", team_prompt, delete_target_header=True)

        return prompt


    @staticmethod
    def load_prompt(project, prompt_name, use_default_prompt=True, prompt_dir:str=None)->str:
        filename = Paths().get_agent_prompt_file_name(prompt_name)

        prompt = SystemPrompt.load_statement_file(project, filename, prompt_dir)

        if prompt is None and use_default_prompt:
            prompt = "Ты - сообразительный и остроумный ассистент-помощник"

        return prompt

    @staticmethod
    def load_statement_file(project, filename, prompt_dir:str=None) -> str:

        #1е место для поиска - папка с проектом
        if Paths().project_artifact_exists(project, artifact=filename):
            prompt = read_project_file(project, filename)
            used_prompt = str(Paths().get_project_artifact(project, artifact=filename))
            logger.trace(f"project [{project}], statement file [{filename}]. using path to load: {used_prompt} ")
            return prompt
        #1.5 место для поиска - prompt_dir
        if prompt_dir is not None:
            prompt = read_file(prompt_dir, filename)
            used_prompt = prompt_dir + "." + filename
            logger.trace(f"project [{project}], statement file [{filename}]. using path to load: {used_prompt} ")
            return prompt

        # 2е место для поиска - папка src/agents/prompts
        prompt = read_file(Paths().agent_prompts, filename)
        used_prompt = env_var_path_prompts_default + "." + filename
        logger.trace(f"project [{project}], statement file [{filename}]. using path to load: {used_prompt} ")

        return prompt