from abc import ABC, abstractmethod
from openai import OpenAI
from langchain_ollama.chat_models import  ChatOllama
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

from utils.sugar import substring_after

load_dotenv()

openrouter_key = os.getenv("OPENROUTER_API_KEY")
bothub_key = os.getenv("BOTHUB_API_KEY")


# 648 184

class LLM(ABC):

    def __init__(self, key: str, url: str, model: str = None):
        self.key = key
        self.url = url
        self.model = model

    @abstractmethod
    def prompt(self, prompt: str, prev_messages: list | None = None, temperature: float = 0.0) -> str:
        pass

    @abstractmethod
    def request(self, messages: list, temperature: float = 0.0) -> str:
        pass

class LlmGate():

    _aliveModel: LLM | None = None

    def __init__(self):
        self.models = []
        #self.models.append(Qwen38b())
        self.models.append(OpenRouterDeepseekChatV30324_3())
        self.models.append(OpenRouterDeepseekChatV30324_2())
        self.models.append(OpenRouterDeepseekChatV30324())
        self.models.append(BotHubDeepseekChatV30324Free())
        #self.models.append(BotHubDeepseekChatV30324())
        #self.models.append(BotHubGemini2Flash())

    def get_active_model_name(self):
        return  self._aliveModel.__class__.__name__

    def prompt(self, prompt: str, prev_messages: list | None = None, temperature: float = 0.0) -> str:
        messages = (prev_messages if prev_messages is not None else []) + [{'role': 'user', 'content': prompt}]
        return self.request(messages, temperature)[0]

    def _request_active_model(self, messages: list, temperature: float = 0.0)-> (str,str):
        response = self._aliveModel.request(messages, temperature)
        return response, self.get_active_model_name()

    def request(self, messages: list, temperature: float = 0.0) -> (str,str):
        # Сначала пробуем текущую живую модель
        if self._aliveModel is not None:
            try:
                return self._request_active_model(messages, temperature)
            except Exception:
                pass  # начинаем поиск рабочей модели

        # Если живая модель не сработала, ищем первую рабочую среди всех
        # todo: лучше сделать курсор, чтобы не идти по уже заведомо мертвым моделям
        for model in self.models:
            try:
                self._aliveModel = model  # Запоминаем рабочую модель
                return self._request_active_model(messages, temperature)
            except Exception as e:
                print(f"⚠️ gate ({type(e).__name__}): {str(e)}")
                continue  # Пробуем следующую модель

        # Если ни одна модель не сработала
        self._aliveModel = None
        raise Exception("All models failed to respond")


class LLmWithOpenAiApi(LLM):

    def __init__(self, key: str, url: str, model: str = None):
        super().__init__(key, url, model)
        self.client = OpenAI(
            api_key=key,
            base_url=url)

    def prompt(self, prompt: str, prev_messages: list | None = None, temperature: float = 0.0) -> str:
        messages = (prev_messages if prev_messages is not None else []) + [{'role': 'user', 'content': prompt}]
        return self.request(messages, temperature)

    def request(self, messages: list, temperature: float = 0.0) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            temperature=temperature,
            #response_format={"type": "json_object"}
        )
        if chat_completion.model_extra is not None:
            if chat_completion.model_extra.get("error") is not None:
                raise Exception(chat_completion.model_extra["error"]["message"])
        if chat_completion.choices is None:
            raise Exception("No choices")
        res = chat_completion.choices[0].message.content
        return res

    async def aprompt(self, text: str, prev_messages: list | None = None, temperature: float = 0.0) -> str:
        return self.prompt(text, prev_messages, temperature)


class OllamaBased(LLM):

    def __init__(self, model: str):
        super().__init__("", "", model)
        self.client = ChatOllama(model=model, temperature=0, )

    def prompt(self, prompt: str, prev_messages: list | None = None, temperature: float = 0.0) -> str:
        messages =  (prev_messages if prev_messages is not None else [])  + [{'role': 'user', 'content': prompt}]
        return self.request(messages, temperature)

    def request(self, messages: list, temperature: float = 0.0) -> str:
        msgs = self.__build_messages_langchain(messages)
        response = self.client.invoke(msgs)
        return response.content

    async def aprompt(self, text: str, prev_messages: list | None = None, temperature: float = 0.0) -> str:
        return self.prompt(text, prev_messages, temperature)

    @staticmethod
    def __build_messages_langchain(prev_messages: list | None) -> list[BaseMessage]:
        """Возвращает сообщения в формате для LLM (без служебных полей)"""
        langchain_messages = []
        if prev_messages is None:
            return langchain_messages
        for msg in prev_messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
            elif msg["role"] == "system":
                langchain_messages.append(SystemMessage(content=msg["content"]))
        return langchain_messages

class Qwen38b(OllamaBased):
    def __init__(self):
        super().__init__("qwen3:8b")

    def prompt(self, prompt: str, prev_messages: list | None = None, temperature: float = 0.0) -> str:
        s = super().prompt(prompt, prev_messages, temperature)
        res = substring_after(s, "</think>").strip()
        return res

class OpenRouterDeepseekChatV30324(LLmWithOpenAiApi):
    def __init__(self):
        super().__init__(os.getenv("OPENROUTER_API_KEY"),
                         "https://openrouter.ai/api/v1",
                         "deepseek/deepseek-chat-v3-0324:free")

class OpenRouterDeepseekChatV30324_2(LLmWithOpenAiApi):
    def __init__(self):
        super().__init__(os.getenv("OPENROUTER_API_KEY2"),
                         "https://openrouter.ai/api/v1",
                         "deepseek/deepseek-chat-v3-0324:free")

class OpenRouterDeepseekChatV30324_3(LLmWithOpenAiApi):
    def __init__(self):
        super().__init__(os.getenv("OPENROUTER_API_KEY3"),
                         "https://openrouter.ai/api/v1",
                         "deepseek/deepseek-chat-v3-0324:free")


class BotHubDeepseekChatV30324Free(LLmWithOpenAiApi):
    def __init__(self):
        super().__init__(os.getenv("BOTHUB_API_KEY"),
                         "https://bothub.chat/api/v2/openai/v1",
                         "deepseek-chat-v3-0324:free")

class BotHubGemini2Flash(LLmWithOpenAiApi):
    def __init__(self):
        super().__init__(os.getenv("BOTHUB_API_KEY"),
                         "https://bothub.chat/api/v2/openai/v1",
                         "gemini-2.0-flash-001")


class BotHubDeepseekChatV30324(LLmWithOpenAiApi):
    def __init__(self):
        super().__init__(os.getenv("BOTHUB_API_KEY"),
                         "https://bothub.chat/api/v2/openai/v1",
                         "deepseek-chat-v3-0324")
