from datetime import datetime
from importlib.resources import files, as_file
import os

from paths import Paths

def get_project_file_latest(project:str, filename:str, extension:str)->str:
    dir = Paths().get_path_in_project_artifacts_dir(project)
    std_files = []

    # Проходим по всем файлам в директории
    for f in os.listdir(dir):
        if f.lower().startswith(f"{filename.lower()}.") and f.lower().endswith(f".{extension.lower()}"):
            try:
                # Извлекаем дату и время из имени файла
                date_part = f[len(filename)+1:-(len(extension)+1)]  # Убираем "STD." и ".md"
                file_datetime = datetime.strptime(date_part, "%Y-%m-%d_%H-%M-%S")
                std_files.append((file_datetime, f))
            except ValueError:
                std_files.append( (datetime(2000, 1, 1), f ))  # Пропускаем файлы с некорректным форматом

    if not std_files:
        return None

    # Сортируем файлы по дате (от новых к старым)
    std_files.sort(reverse=True, key=lambda x: x[0])

    # Возвращаем имя самого свежего файла
    latest_file = std_files[0][1]
    return os.path.join(dir, latest_file)


def read_project_file(project:str, filename:str)->str:
    return read_file(Paths().get_rel_path_in_project_artifacts_dir(project), filename)


def write_project_file(project:str, filename:str, text:str):
    write_file(Paths().get_rel_path_in_project_artifacts_dir(project), filename, text)

def read_file(package:str, filename:str)->str|None:
    data_file = files(package).joinpath(filename)
    if not data_file.is_file():
        return None
    with as_file(data_file) as f:
        data = f.read_text(encoding="utf-8")
    return data


def write_file(package_or_dir:str, filename:str, text:str):
    root = Paths().get_source_root()
    dir = root / package_or_dir.replace(".", "/")
    dir.mkdir(parents=True, exist_ok=True)
    output_file = dir / filename
    output_file.write_text(text, encoding="utf-8")
