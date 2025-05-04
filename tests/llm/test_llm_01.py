import re
import pytest
from src.llm.LlmGate import LlmGate, OpenRouterDeepseekChatV30324,BotHubDeepseekChatV30324Free

def clean(s:str)->str:
    return (re.sub(r"[^a-zA-Z0-9а-яА-ЯёЁ]", "",s)
            .lower())

def test_OpenRouterDeepseekChatV30324():
    chat = OpenRouterDeepseekChatV30324()
    resp = chat.prompt("say 'hello, world'")
    assert clean(resp) == clean('Hello, world!')

def test_BotHubDeepseekChatV30324():
    chat = BotHubDeepseekChatV30324Free()
    resp = chat.prompt("say 'hello, world'")
    print()
    print(resp)
    print(clean(resp))
    print(clean('Hello, world!'))
    assert clean(resp) == clean('Hello, world!')

def test_LlmGate():
    gate = LlmGate()
    resp = gate.prompt("say 'hello, world'")
    print()
    assert clean(resp) == clean('Hello, world!')

@pytest.mark.asyncio
async def test_Async():
    chat = OpenRouterDeepseekChatV30324()
    resp = await chat.aprompt("say 'hello, world'")
    print(resp)
    assert clean(resp) == clean('Hello, world!')