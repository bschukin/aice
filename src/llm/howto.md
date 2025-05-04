В OpenAI Chat API объект `messages` поддерживает несколько типов сообщений с разными полями. Вот **полный набор** того, что можно добавить:

### 1. Базовые типы сообщений

#### System Message (устанавливает поведение ассистента)
```python
{
    "role": "system",
    "content": "You are a helpful assistant that speaks like a pirate.",
    "name": "system_settings"  # опционально
}
```

#### User Message (ввод пользователя)
```python
{
    "role": "user",
    "content": "What's the weather today?",
    "name": "john_doe"  # опционально (для мульти-юзерных чатов)
}
```

#### Assistant Message (предыдущие ответы ассистента)
```python
{
    "role": "assistant",
    "content": "Arr! The weather be sunny today!",
    "name": "pirate_bot"  # опционально
}
```

### 2. Function/Tool Calling (для работы с функциями)

#### Запрос на вызов функции (от ассистента)
```python
{
    "role": "assistant",
    "content": None,
    "tool_calls": [
        {
            "id": "call_abc123",
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "arguments": '{"location":"Boston"}'
            }
        }
    ]
}
```

#### Результат выполнения функции
```python
{
    "role": "tool",
    "content": '{"temperature":22, "unit":"celsius"}',
    "tool_call_id": "call_abc123"  # обязательное поле
}
```


### 4. Все возможные поля

| Поле | Обязательное | Описание |
|------|--------------|----------|
| `role` | Да | `system`/`user`/`assistant`/`tool` |
| `content` | Да* | Текст (*может быть `None` для assistant с tool_calls) |
| `name` | Нет | Идентификатор отправителя |
| `tool_calls` | Нет | Только для `role: assistant` |
| `tool_call_id` | Да для `role: tool` | Соответствует `id` из `tool_calls` |


### Важные нюансы:
1. **Порядок сообщений** должен сохранять хронологию
2. **System-сообщение** должно быть первым (если присутствует)

-----

Чтобы системный промпт с постановкой задачи не терялся в истории сообщений, есть несколько проверенных стратегий. Вот оптимальные варианты:

### 1. **System-промпт в начале (рекомендуемый способ)**
```python
messages = [
    {"role": "system", "content": "Твой промпт с задачей (50-100 слов)"},  # Фиксируется в начале
    *history[-10:],  # Последние 10 сообщений истории
    {"role": "user", "content": "Текущий запрос"}
]
```
**Почему работает**:  
- Модель сильнее всего учитывает первый system-промпт  
- OpenAI специально обучали модели обращать внимание на system-сообщения  

### 2. **Периодическое напоминание (для длинных диалогов)**
```python
if len(history) % 5 == 0:  # Каждые 5 сообщений
    messages.insert(-1, {"role": "system", "content": "Напоминание ключевых требований"})
```

### 3. **Сворачивание истории + промпт**
```python
context = "\n".join(f"{m['role']}: {m['content']}" for m in history[:-5])
prompt = f"""Твоя задача: {task_prompt}\n\nКонтекст:\n{context}"""

messages = [
    {"role": "system", "content": prompt},
    {"role": "user", "content": history[-1]["content"]}
]
```

### 4. **Двойной промптинг (для критичных задач)**
```python
messages = [
    {"role": "system", "content": task_prompt},
    *history[-6:],
    {"role": "assistant", "content": "Я помню, что нужно: " + task_summary}
]
```

### 5. **Динамический рефрейминг (продвинутый способ)**
```python
def frame_prompt(task, history):
    relevant_history = analyze_and_select(history)  # NLP-анализ релевантности
    return f"""{task}
    
    Relevant context:
    {relevant_history}"""

messages = [
    {"role": "system", "content": frame_prompt(task_prompt, history)},
    {"role": "user", "content": "Текущий запрос"}
]
```

### Критерии выбора:
1. **Для коротких диалогов** (<15 сообщений) – достаточно system-промпта в начале  
2. **Для длинных сессий** – комбинируйте 1+2 (фиксированный промпт + напоминания)  
3. **Для сложных задач** – используйте 3 или 4 подход  

**Важно**:  
- Держите промпт лаконичным (не более 150 слов)  
- Ключевые требования лучше дублировать в начале последнего user-сообщения:  
  ```python
  {"role": "user", "content": f"Важно: {key_requirement}\n\n{question}"}
  ```  

Тестируйте разные варианты – эффективность может зависеть от конкретной модели (GPT-3.5 vs GPT-4) и сложности задачи.