

def iif(condition:bool, if_true, if_false):
    if condition:
        return if_true
    else:
        return if_false

def elvis(value, default):
    return value if value is not None else default

def is_empty_or_whitespace(s):
    return not s.strip()

def substring_before(s, delimiter):
    """Аналог Kotlin's subStringBefore()"""
    index = s.find(delimiter)
    return s[:index] if index != -1 else s


def substring_after(s: str, delimiter: str, save_delimiter: bool = False) -> str:
    """Аналог Kotlin's subStringAfter() с дополнительной опцией сохранения разделителя.

    Args:
        s: Исходная строка
        delimiter: Разделитель
        save_delimiter: Если True, разделитель сохраняется в результате

    Returns:
        Подстрока после первого вхождения разделителя (включая сам разделитель, если save_delimiter=True)
        Пустая строка, если разделитель не найден
    """
    index = s.find(delimiter)
    if index == -1:
        return s

    return s[index:] if save_delimiter else s[index + len(delimiter):]


def substring_before_last(s: str, delimiter: str, save_delimiter: bool = False) -> str:
    """Аналог Kotlin's subStringBeforeLast() с возможностью сохранить разделитель.

    Args:
        s: Исходная строка
        delimiter: Разделитель
        save_delimiter: Если True, разделитель сохраняется в конце результата

    Returns:
        Подстрока до последнего вхождения разделителя (включая сам разделитель в конце, если save_delimiter=True)
        Вся строка, если разделитель не найден
    """
    index = s.rfind(delimiter)
    if index == -1:
        return s

    return s[:index + len(delimiter)] if save_delimiter else s[:index]


def ends_with(s: str, suffix: str, ignore_case: bool = False) -> bool:
    if ignore_case:
        return s.lower().endswith(suffix.lower())
    return s.endswith(suffix)