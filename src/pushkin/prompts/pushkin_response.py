#AI-ассистент руководителя. Схема ответов.
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


# --- Классы для инкрементных изменений ---
class ChangeItem(BaseModel):
    """Одно изменение в документе .MD (STD, HRD, ...). Каждая изменяющаяся строка идет как отдельный экземпляр ChangeItem"""
    type: Literal["add", "edit", "delete", "move"] = Field(None, description="Тип операции")
    sections: Optional[list[str]] = Field(None, description="Локация в  разделах уровня '#', '##', '###' и тд. (например STD: ['Долгосрочные цели', 'Цели 2025', 'Основать направление ИИ в компании']), HRD:['Департамент', 'Карточка сотрудника']). Если тип операции - 'delete' и удаляется раздел целиком, можно указать только sections, не указывая old_text, new_text")
    old_text: Optional[str] = Field(None, description="Исходный текст для замены/удаления. Текст должен содержать одну строку целиком, без переносов строки")
    new_text: Optional[str] = Field(None, description="Новый текст (для add/edit). Текст должен содержать строку целиком, без переносов строки '\n'. Если строка не является разделом ('#', '##'), добавляй в начало символ '- ' ")


class ConflictAlert(BaseModel):
    """Конфликт при изменении"""
    description: str = Field(description="Пересечение сроков с задачей 'Реестр сервисов'")
    suggested_solution: str = Field(description="Перенести на июль или уменьшить объем")


# --- Основной формат ответа ---
class AiAgentResponse(BaseModel):
    """Структура ответа с инкрементными изменениями"""
    for_human: str = Field(default="Изменения сделаны!", description="Пояснение на естественном языке (Markdown)")

    # Инкрементные изменения в изменяемый документ (STD, HRD)
    changes_made: Optional[List[ChangeItem]] = Field(None, description="Список примененных изменений")
    conflicts: Optional[List[ConflictAlert]] = Field(None, description="Обнаруженные конфликты")

    # Только для критичных изменений
    requires_confirmation: bool = Field(False, description="Требует подтверждения пользователем")

    # Полный документ (STD, HRD) передается ТОЛЬКО при явном запросе
    # Например, если просят дать полный текст документа, или отформатировать его или представить в отсортированном особым образом виде
    full_document: Optional[str] = Field(None, description="Полный текст документа, если явно запрошен")