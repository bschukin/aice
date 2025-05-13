import json
from datetime import datetime

from agents.baseagent import BaseAgent
from agents.system_prompt import SystemPrompt
from pushkin.prompts.pushkin_commands_schema import PushkinResponse
from utils.file_io import read_project_file, write_project_file, get_project_file_latest
from utils.sugar import substring_after, substring_before_last


class Pushkin(BaseAgent):

    def __init__(self, name: str = "Pushkin", project:str='pushkin'):
        super().__init__(role="pushkin", name=name, project=project, prompt_dir="src.pushkin.prompts")
        self._std_example = SystemPrompt.load_statement_file(project, "STD.example.md", prompt_dir =self._prompt_dir)
        self._response_schema = SystemPrompt.load_statement_file(project, "pushkin_commands_schema.py", prompt_dir =self._prompt_dir, )

    def _get_system_prompt(self) -> list[dict[str, str]]:
        nsb0 = """
        
            Ты отвечаешь только в формате JSON.
            
        """
        std = read_project_file(self._project, get_project_file_latest(self._project, "STD", "md"))
        nsb = """
                ================
                **ВАЖНО**: Ответ дается только в формате JSON! (pydantic класс PushkinResponse). 
                **NB: ЗАПРЕЩАЕТСЯ самостоятельно менять контент, который не менялся по запросу Руководителя.
                То есть, содержимое документа в новой версии должно строго соответствовать содержимому в старой, за исключением
                новых, измененных или удаленных пунктов.**
                проверь себя на соблюдение данных условий перед ответом.
                Если ты изменишь контент, удалишь нужные руководителю строчки, он будет очень печален.
                """

        agent_prompt = {'role': 'system', 'content': self._prompt.agent_prompt
                                                     + "\r\n================\r\n" + self._std_example
                                                    + "\r\n================\r\n" + self._response_schema}
        current_std = {'role': 'system', 'content':
            """
                # STD - Strategic Tasks Document - Долгосрочный список целей и задач руководителя
                **NB: Текущее состояние документа Strategic Tasks Document - Долгосрочный список целей и задач руководителя**
                
            """ +
            std}

        nb = {'role': 'system', 'content': nsb}
        nb0 = {'role': 'system', 'content': nsb0}
        return [nb0, agent_prompt,  current_std, nb]

    def _parse_agent_response(self, json_data)->str:
        try:
            cleanead = self.extract_json(json_data)

            data_dict = json.loads(cleanead)
            if data_dict is None:
                return json_data + "   @raw"
            pr = PushkinResponse.model_validate(data_dict)

            if pr.STD is not None:
                filename= f"STD.{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.MD"
                write_project_file(self._project, filename, pr.STD.text)

            return pr.for_human

        except Exception as e:  # 'as e' сохраняет исключение в переменную e
            print(f"Произошла ошибка: {e}")  # Печатаем ошибку
            return  json_data + "   @raw"

    @staticmethod
    def extract_json(json_data) -> str:
        s = substring_after(json_data, "{", save_delimiter=True)
        s = substring_before_last(s, "}", save_delimiter=True)
        return s