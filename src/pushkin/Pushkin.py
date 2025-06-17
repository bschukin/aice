import json
from datetime import datetime

from agents.baseagent import BaseAgent
from agents.system_prompt import SystemPrompt
from pushkin.prompts.pushkin_commands_schema import PushkinResponse
from utils.file_io import read_project_file, write_project_file, get_project_file_latest
from utils.md import apply_md_changes
from utils.sugar import substring_after, substring_before_last


class Pushkin(BaseAgent):

    def __init__(self, name: str = "Pushkin", project: str = 'pushkin'):
        super().__init__(role="pushkin", name=name, project=project, prompt_dir="src.pushkin.prompts")
        self._std_example = SystemPrompt.load_statement_file(project, "STD.example.md", prompt_dir=self._prompt_dir)
        self._response_schema = SystemPrompt.load_statement_file(project, "pushkin_commands_schema.py",
                                                                 prompt_dir=self._prompt_dir, )

    def get_STD(self) -> str:
        return read_project_file(self._project, get_project_file_latest(self._project, "STD", "md"))

    def _get_system_prompt(self) -> list[dict[str, str]]:
        nsb0 = """
        
            Ты отвечаешь только в формате JSON.
            
        """

        nsb = """
                ================
                **ВАЖНО**: Ответ дается только в формате JSON! (pydantic класс PushkinResponse). 
                **NB: ЗАПРЕЩАЕТСЯ самостоятельно менять контент, который не менялся по запросу Руководителя.
                То есть, содержимое документа в новой версии должно строго соответствовать содержимому в старой, за исключением
                новых, измененных или удаленных пунктов.**
                проверь себя на соблюдение данных условий перед ответом.
                """

        agent_prompt = {'role': 'system', 'content': self._prompt.agent_prompt
                                                     + "\r\n============\r\n" + "В качестве примера будет передана полная текущая версия STD. ЕЕ и следует изменять. "
                                                     + "\r\n============\r\n" + self._response_schema}
        current_std = {'role': 'system', 'content':
            """
            **Strategic Tasks Document. Текущее состояние документа:**
            
            """ +
            self.get_STD()}

        nb = {'role': 'system', 'content': nsb}
        nb0 = {'role': 'system', 'content': nsb0}
        return [nb0, agent_prompt, current_std]

    def _parse_agent_response(self, json_data) -> str:
        try:
            cleanead = self.extract_json(json_data)

            data_dict = self.load_dict_from_json(cleanead)
            if data_dict is None:
                return json_data + "   @raw"
            pr = PushkinResponse.model_validate(data_dict)

            if pr.changes_made:
                text = apply_md_changes(self.get_STD(), pr)
                filename = f"STD.{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.MD"
                write_project_file(self._project, filename, text)

            if pr.full_std:
                assert pr.changes_made is None or len(pr.changes_made) == 0
                text = pr.full_std
                filename = f"STD.{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.MD"
                write_project_file(self._project, filename, text)

            return pr.for_human

        except Exception as e:  # 'as e' сохраняет исключение в переменную e
            print(f"Произошла ошибка: {e}")  # Печатаем ошибку
            return json_data + "   @raw"

    def load_dict_from_json(self, cleanead)->dict:
        dict =  json.loads(cleanead)
        if "change_made" in dict:
            assert "changes_made" not in dict
            dict["changes_made"] = dict["change_made"]
        return dict

    @staticmethod
    def extract_json(json_data) -> str:
        s = substring_after(json_data, "{", save_delimiter=True)
        s = substring_before_last(s, "}", save_delimiter=True)
        return s
