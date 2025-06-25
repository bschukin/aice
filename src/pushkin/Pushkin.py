import json
from datetime import datetime
from typing import cast

from agents.baseagent import BaseAgent
from agents.prompts.commands_schema import ParsedResponse
from agents.system_prompt import SystemPrompt
from pushkin.prompts.pushkin_response import PushkinResponse
from utils.dates import get_current_datetime_info
from utils.file_io import read_project_file, write_project_file, get_project_file_latest
from utils.md import apply_md_changes
from utils.sugar import substring_after, substring_before_last
import traceback


class Pushkin(BaseAgent):

    def __init__(self, name: str = "Pushkin", project: str = 'pushkin'):

        super().__init__(role="pushkin", name=name, project=project, prompt_dir="src.pushkin.prompts")
        self._response_schema = SystemPrompt.load_statement_file(project, "pushkin_response.py",
                                                                 prompt_dir=self._prompt_dir, )

    def get_STD(self) -> str:
        return read_project_file(self._project, get_project_file_latest(self._project, "STD", "md"))

    def _get_system_prompt(self) -> list[dict[str, str]]:

        curr_date = {'role': 'system', 'content': get_current_datetime_info()}
        agent_prompt = {'role': 'system', 'content': self._prompt.agent_prompt}
        responce_schema = {'role': 'system', 'content': self._response_schema}
        current_std = {'role': 'system', 'content':self.get_STD()}

        return [curr_date, agent_prompt, responce_schema, current_std]

    def _parse_agent_response(self, json_data) -> ParsedResponse:
        try:
            cleanead = self.extract_json(json_data)

            data_dict = self.load_dict_from_json(cleanead)
            if data_dict is None:
                return ParsedResponse(isError=True, error_response=json_data)
            pr = PushkinResponse.model_validate(data_dict)
            return ParsedResponse(human_response=pr.for_human, formatted_response=cleanead, pydantic_result=pr)

        except Exception as e:  # 'as e' сохраняет исключение в переменную e
            print(f"Произошла ошибка: {e}")  # Печатаем ошибку
            traceback.print_exc()  # Выводит полный трейсбек ошибки
            return ParsedResponse(isError=True, error_response=json_data)

    def _process_agent_response(self, prs:ParsedResponse) -> ParsedResponse:
        pr:PushkinResponse = cast(PushkinResponse, prs.pydantic_result)

        if pr.changes_made:
            text = apply_md_changes(self.get_STD(), pr)
            filename = f"STD.{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.MD"
            write_project_file(self._project, filename, text)

        if pr.full_std:
            assert pr.changes_made is None or len(pr.changes_made) == 0
            text = pr.full_std
            filename = f"STD.{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.MD"
            write_project_file(self._project, filename, text)

        return prs

    def load_dict_from_json(cls, cleanead)->dict:
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
