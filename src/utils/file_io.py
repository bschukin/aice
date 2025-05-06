from importlib.resources import files, as_file


from paths import Paths

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
