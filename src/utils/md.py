from rich.console import Console
from rich.markdown import Markdown

console = Console()

def print_markdown(text):
    md = Markdown(text)
    console.print(md)


def insert_section_into_markdown(content, target_header, new_content, delete_target_header:bool=False)->str:
    """
    Вставляет новый раздел после указанного заголовка в Markdown содержимое.

    :param content: Строка с содержимым MD файла
    :param target_header: Заголовок, после которого нужно вставить новый раздел (например, "# Схема")
    :param new_content: Содержимое нового раздела
    :return: Модифицированное содержимое
    """
    lines = content.split('\n')
    new_section = f"\n{new_content}\n"
    result = []
    found = False

    for line in lines:
        if line.strip() == target_header and not found:
            if not delete_target_header:
                result.append(line)
            result.append(new_section)
            found = True
        else:
            result.append(line)

    return '\n'.join(result)