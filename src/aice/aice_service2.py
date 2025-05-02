key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMjc0OTRlLWI1NTEtNGFjNy1iZTA0LTQ4NDEzMjdlZjZmMiIsImlzRGV2ZWxvcGVyIjp0cnVlLCJpYXQiOjE3NDQxNjg5MzksImV4cCI6MjA1OTc0NDkzOX0.N3aznEtLa9odiM4P0p5qhdZAU_QFfgu8Zox5sXDO7k8'

from  src.aice.aice_service import _build_prompt
from  src.aice.aice_service import _strip_json
from openai import OpenAI


def generate_command( text:str):
    prompt = _build_prompt(text)

    client = OpenAI(
        api_key=key,
        base_url='https://bothub.chat/api/v2/openai/v1'
    )
    print(f"client.chat: {text}")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': prompt,
            }
        ],
        model='deepseek-chat-v3-0324:free',
        temperature=0.0
    )
    #return chat_completion.choices[0].message.content
    #print(f"chat_completion: {text}")
    res =  _strip_json(chat_completion.choices[0].message.content)
    return res