import json
from abc import ABC

from agents.prompts.commands_schema import AgentResponse
from agents.system_prompt import SystemPrompt
from llm.llm_gate import LlmGate
from agents.message_history import MessageHistory
from src.utils.sugar import substring_after, substring_before_last, ends_with


class BaseAgent(ABC):
    __gate = LlmGate()

    def _gate(self):
        return self.__gate

    def __init__(self, role: str, name: str, project: str = 'default', prompt_dir: str = None):
        self._role = role  # Защищенное поле (по соглашению)
        self._name = name
        self._project = project
        self._prompt_dir = prompt_dir
        self._prompt = SystemPrompt(role, project, prompt_dir)
        self._history = MessageHistory(project, role)

    @property
    def role(self) -> str:
        """Метод для получения роли"""
        return self._role

    @property
    def name(self) -> str:
        """Метод для получения имени"""
        return self._name

    def dump_state(self):
        self._history.dump_to_file()

    def reset_state(self):
        self._history.delete_all_history()

    def _get_system_prompt(self) -> list[dict[str, str]]:
        agent_prompt = {'role': 'system', 'content': self._prompt.agent_prompt}
        return [agent_prompt]

    def chat(self, prompt: str, temperature=0.0) -> str:
        messages = (self._get_system_prompt()
                    + self._history.get_prepared_messages()
                    + [{'role': 'user', 'content': prompt}])

        resp = self.__gate.request(messages, temperature)

        parsed_resp = self._parse_agent_response(resp)
        is_error = ends_with(parsed_resp, "@raw")

        self._history.add_message("user", prompt)
        if is_error is not True:
            self._history.add_message("assistant", content=parsed_resp, tech_content=resp)
        else:
            self._history.add_message("assistant", content=resp, tech_content=resp, error=True)

        print("================")
        return parsed_resp

    def _parse_agent_response(self, json_data) -> str:
        cleanead = self.__extract_json(json_data)
        data_dict = json.loads(cleanead)
        ar = AgentResponse.model_validate(data_dict)
        print(ar)
        return ar.for_human

    @staticmethod
    def __extract_json(json_data) -> str:
        s = substring_after(json_data, "{", save_delimiter=True)
        s = substring_before_last(s, "}", save_delimiter=True)
        return s
