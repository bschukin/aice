import json
from abc import ABC

from agents.prompts.commands_schema import AgentResponse
from agents.system_prompt import SystemPrompt
from llm.llm_gate import LlmGate
from agents.message_history import MessageHistory
from src.utils.sugar import substring_after, substring_before_last


class BaseAgent(ABC):
    __gate = LlmGate()

    def __init__(self, role: str, name: str, project: str = 'default', prompt_dir:str=None):
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
        #self.__parse_agent_response(resp)
        self._history.add_message("user", prompt)
        self._history.add_message("assistant", resp)
        print("================")
        return resp

    def __parse_agent_response(self, json_data):
        cleanead = self.__extract_json(json_data)
        print(cleanead)
        data_dict = json.loads(cleanead)
        ar = AgentResponse.model_validate(data_dict)
        print(ar)

    @staticmethod
    def __extract_json(json_data) -> str:
        s = substring_after(json_data, "{", save_delimiter=True)
        s = substring_before_last(s, "}", save_delimiter=True)
        return s
