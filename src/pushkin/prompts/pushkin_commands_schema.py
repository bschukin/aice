# Пушкин — AI-ассистент руководителя (v2.0)
from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


# --- Классы для инкрементных изменений ---
class ChangeItem(BaseModel):
    """Одно изменение в STD"""
    type: Literal["add", "edit", "delete", "move"] = Field(..., description="Тип операции")
    section: str = Field(..., description="Раздел (например, Долгосрочные/Среднесрочные/Постоянные)")
    subsection: Optional[str] = Field(None, description="Подраздел (например 'Безопасная разработка')")
    old_text: Optional[str] = Field(None, description="Исходный текст для замены/удаления")
    new_text: Optional[str] = Field(None, description="Новый текст (для add/edit)")


class ConflictAlert(BaseModel):
    """Конфликт при изменении"""
    description: str = Field(example="Пересечение сроков с задачей 'Реестр сервисов'")
    suggested_solution: str = Field(example="Перенести на июль или уменьшить объем")


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

