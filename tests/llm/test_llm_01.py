print("0000000000000")
import re
import pytest

from llm.llm_gate import Qwen38b, OpenRouterDeepseekChatV30324_2
from src.llm.llm_gate import LlmGate, OpenRouterDeepseekChatV30324,BotHubDeepseekChatV30324Free

def clean(s:str)->str:
    return (re.sub(r"[^a-zA-Z0-9а-яА-ЯёЁ]", "",s)
            .lower())
test_prompt = "say exactly two words: 'hello, world'. check your response before sending it - it should contain only two words 'hello, world' "

def test_OpenRouterDeepseekChatV30324():
    chat = OpenRouterDeepseekChatV30324_2()
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
    chat = Qwen38b()
    resp = await chat.aprompt(test_prompt)
    print(resp)
    assert clean(resp) == clean('Hello, world!')

def test_Qwen38b():
    chat = Qwen38b()
    resp = chat.prompt(test_prompt)
    print(resp)
    assert clean(resp) == clean('Hello, world!')
