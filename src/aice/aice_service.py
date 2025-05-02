key = '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'

import requests
import json
from pathlib import Path

def generate_command( text:str)->str:
    prompt = _build_prompt(text)

    response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "deepseek/deepseek-chat-v3-0324:free",
                "temperature":0.0,
                "messages": [
                    {
                        "role": "user",
                        "content": f"{prompt}"
                    }
                ],

            })
        )
    response_data = response.json()
    if(response_data['error'] is not None):
        raise ValueError(response_data['error']['message'])
    assert len(response_data['choices']) ==1, "Ответ содержит не один выбор (choice)"

    res:str =   response_data['choices'][0]['message']['content']
    res =  _strip_json(res)
    return res

def _strip_json(json)->str:
    start_index = json.find('{')
    json_str = json[start_index:]
    end_index = json_str.find('```')
    json_str = json_str[:end_index]
    return json_str

def _build_prompt(query:str)->str:

    descr_path = _get_path("prompts/command0.12.txt")
    with open(descr_path, "r", encoding="utf-8") as file:
        prompt = file.read()

    descr_path = _get_path("prompts/fieldsets.txt")
    with open(descr_path, "r", encoding="utf-8") as file:
        prompt = prompt + "\r\n" + file.read()

    return prompt  + "\r\n" + query

def _get_path(path):
    # Получаем абсолютный путь к корню проекта
    PROJECT_ROOT = Path(__file__).parent.parent  # Поднимаемся на 2 уровня вверх от текущего файла
    # Формируем путь к файлу относительно корня
    file_path = PROJECT_ROOT / path
    return file_path