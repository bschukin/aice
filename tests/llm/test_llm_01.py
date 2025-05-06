print("0000000000000")
import re
import pytest

from llm.llm_gate import Ollama8b
from src.llm.llm_gate import LlmGate, OpenRouterDeepseekChatV30324,BotHubDeepseekChatV30324Free

def clean(s:str)->str:
    return (re.sub(r"[^a-zA-Z0-9а-яА-ЯёЁ]", "",s)
            .lower())
test_prompt = "say 'hello, world'"

def test_OpenRouterDeepseekChatV30324():
    chat = OpenRouterDeepseekChatV30324()
    resp = chat.prompt(test_prompt)
    print(resp)
    assert clean(resp) == clean('Hello, world!')

def test_BotHubDeepseekChatV30324Free():
    chat = BotHubDeepseekChatV30324Free()
    resp = chat.prompt(test_prompt)
    print(resp)
    assert clean(resp) == clean('Hello, world!')

def test_LlmGate():
    gate = LlmGate()
    resp = gate.promptNo(test_prompt)
    print(resp)
    assert clean(resp) == clean('Hello, world!')

@pytest.mark.asyncio
async def test_Async():
    chat = Ollama8b()
    resp = await chat.aprompt(test_prompt)
    print(resp)
    assert clean(resp) == clean('Hello, world!')

def test_Ollama8b():
    chat = Ollama8b()
    resp = chat.prompt(test_prompt)
    print(resp)
    assert clean(resp) == clean('Hello, world!')
