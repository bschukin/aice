from abc import ABC, abstractmethod
from openai import OpenAI

openrouter_key = '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'
bothub_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMjc0OTRlLWI1NTEtNGFjNy1iZTA0LTQ4NDEzMjdlZjZmMiIsImlzRGV2ZWxvcGVyIjp0cnVlLCJpYXQiOjE3NDQxNjg5MzksImV4cCI6MjA1OTc0NDkzOX0.N3aznEtLa9odiM4P0p5qhdZAU_QFfgu8Zox5sXDO7k8'


class LlmGate():

    def __init__(self):
        self.models = []
        self.models.append(OpenRouterDeepseekChatV30324())
        self.models.append(BotHubDeepseekChatV30324())

    def prompt(self, prompt: str, temperature: float = 0.0) -> str:
        return self.models[0].prompt(prompt, temperature)


class LLM(ABC):

    def __init__(self, key: str, url: str, model: str = None):
        self.key = key
        self.url = url
        self.model = model

    @abstractmethod
    def prompt(self, prompt: str, temperature: float = 0.0) -> str:
        pass


class LLmWithOpenAiApi(LLM):

    def __init__(self, key: str, url: str, model: str = None):
        super().__init__(key, url, model)
        self.client = OpenAI(
            api_key=key,
            base_url=url)

    def prompt(self, prompt: str, temperature: float = 0.0) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[{
                'role': 'user',
                'content': prompt}],
            model=self.model,
            temperature=temperature
        )
        return chat_completion.choices[0].message.content

    async def aprompt(self, text: str, temperature: float = 0.0) -> str:
        return self.prompt(text, temperature)


class OpenRouterDeepseekChatV30324(LLmWithOpenAiApi):
    def __init__(self):
        super().__init__(openrouter_key,
                         "https://openrouter.ai/api/v1",
                         "deepseek/deepseek-chat-v3-0324:free")


class BotHubDeepseekChatV30324(LLmWithOpenAiApi):
    def __init__(self):
        super().__init__(bothub_key,
                         "https://bothub.chat/api/v2/openai/v1",
                         "deepseek-chat-v3-0324:free")
