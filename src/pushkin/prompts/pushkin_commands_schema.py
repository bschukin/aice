# Пушкин — AI-ассистент руководителя (v2.0)
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


# --- Классы для инкрементных изменений ---
class ChangeItem(BaseModel):
    """Одно изменение в STD"""
    type: Literal["add", "edit", "delete", "move"] = Field(None, description="Тип операции")
    sections: Optional[list[str]] = Field(None, description="Локация в  разделах уровня '#', '##', '###' и тд. (например ['Долгосрочные цели', 'Цели 2025', 'Основать направление ИИ в компании']). Если тип операции - 'delete' и удаляется раздел целиком, можно указать только sections, не указывая old_text, new_text")
    old_text: Optional[str] = Field(None, description="Исходный текст для замены/удаления")
    new_text: Optional[str] = Field(None, description="Новый текст (для add/edit). Текст должен содержать строку целиком, без переносов строки '\n'. Если строка не является разделом ('#', '##'), добавляй в начало символ '- ' ")


class ConflictAlert(BaseModel):
    """Конфликт при изменении"""
    description: str = Field(description="Пересечение сроков с задачей 'Реестр сервисов'")
    suggested_solution: str = Field(description="Перенести на июль или уменьшить объем")


# --- Основной формат ответа ---
class PushkinResponse(BaseModel):
    """Структура ответа с инкрементными изменениями"""
    for_human: str = Field(default="Изменения сделаны!", description="Пояснение на естественном языке (Markdown)")

    # Инкрементные изменения вместо полного STD
    changes_made: Optional[List[ChangeItem]] = Field(None, description="Список примененных изменений")
    conflicts: Optional[List[ConflictAlert]] = Field(None, description="Обнаруженные конфликты")

    # Только для критичных изменений
    requires_confirmation: bool = Field(False, description="Требует подтверждения пользователем")

    # Полный STD передается ТОЛЬКО при явном запросе
    full_std: Optional[str] = Field(None, description="Полный текст STD только если запрошено")

