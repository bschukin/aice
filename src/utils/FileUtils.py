from importlib.resources import files, as_file
from pathlib import Path

def read_project_file(project:str, filename:str)->str:
    return read_file("data."+project, filename)

def write_project_file(project:str, filename:str, text:str):
    write_file("data."+project, filename, text)


def read_file(package:str, filename:str)->str:
    data_file = files(package).joinpath(filename)
    with as_file(data_file) as f:
        data = f.read_text(encoding="utf-8")
    return data


def write_file(package_or_dir:str, filename:str, text:str):
    root = get_source_root()
    dir = root / package_or_dir.replace(".", "/")
    dir.mkdir(parents=True, exist_ok=True)
    output_file = dir / filename
    output_file.write_text(text, encoding="utf-8")

def get_project_path(project:str)->Path:
    pr = "data."+project
    root = get_source_root()
    dir = root / pr.replace(".", "/")
    dir.mkdir(parents=True, exist_ok=True)
    return dir


def get_source_root() -> Path:
    """Возвращает абсолютный путь до корня проекта."""
    current_dir = Path(__file__).parent
    while True:
        if (current_dir / "pyproject.toml").exists():
            return current_dir
        if current_dir == current_dir.parent:  # Дошли до корня файловой системы
            raise FileNotFoundError("Не удалось найти корень проекта (pyproject.toml не обнаружен)")
        current_dir = current_dir.parent
