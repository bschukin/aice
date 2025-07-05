import json
from datetime import datetime
from typing import cast

from agents.baseagent import BaseAgent
from agents.prompts.commands_schema import ParsedResponse
from agents.system_prompt import SystemPrompt
from pushkin.prompts.pushkin_response import AiAgentResponse
from utils.dates import get_current_datetime_info
from utils.file_io import read_project_file, write_project_file, get_project_file_latest
from utils.md import apply_md_changes
from utils.sugar import substring_after, substring_before_last
import traceback


class Stalin(BaseAgent):

    def __init__(self, name: str = "Stalin", project: str = 'stalin'):

        super().__init__(role="stalin", name=name, project=project, prompt_dir="src.stalin.prompts")
        self._response_schema = SystemPrompt.load_statement_file("pushkin", "pushkin_response.py",
                                                                 prompt_dir="src.pushkin.prompts", )

    def get_HRD(self) -> str:
        return read_project_file(self._project, get_project_file_latest(self._project, "HRD", "md"))

    def _get_system_prompt(self) -> list[dict[str, str]]:

        curr_date = {'role': 'system', 'content': get_current_datetime_info()}
        agent_prompt = {'role': 'system', 'content': self._prompt.agent_prompt}
        responce_schema = {'role': 'system', 'content': self._response_schema}
        current_std = {'role': 'system', 'content':self.get_HRD()}

        return [curr_date, agent_prompt, responce_schema, current_std]

    def _parse_agent_response(self, json_data) -> ParsedResponse:
        try:
            cleanead = self.extract_json(json_data)

            data_dict = self.load_dict_from_json(cleanead)
            if data_dict is None:
                return ParsedResponse(isError=True, error_response=json_data)
            pr = AiAgentResponse.model_validate(data_dict)
            return ParsedResponse(human_response=pr.for_human, formatted_response=cleanead, pydantic_result=pr)

        except Exception as e:  # 'as e' сохраняет исключение в переменную e
            print(f"Произошла ошибка: {e}")  # Печатаем ошибку
            traceback.print_exc()  # Выводит полный трейсбек ошибки
            return ParsedResponse(isError=True, error_response=json_data)

    def _process_agent_response(self, prs:ParsedResponse) -> ParsedResponse:
        if prs.isError:
            print("error!!!:" + prs.error_response)
            return prs

        pr:AiAgentResponse = cast(AiAgentResponse, prs.pydantic_result)

        if pr.changes_made:
            text = apply_md_changes(self.get_HRD(), pr)
            filename = f"HRD.{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.MD"
            write_project_file(self._project, filename, text)

        if pr.full_document:
            assert pr.changes_made is None or len(pr.changes_made) == 0
            text = pr.full_document
            filename = f"HRD.{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.MD"
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
