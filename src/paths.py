import os
from dotenv import load_dotenv
from pathlib import Path

from utils.sugar import elvis

load_dotenv(override=True)

env_var_path_data = "path.data"
env_var_path_prompts = "path.agents.prompts"
env_var_path_prompts_default = "src.agents.prompts"
agent_history_file_suffix = ".chat.history.json"
agent_propmt_file_suffix = ".prompt.md"


class Paths:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        cls.data_dir = elvis(os.getenv(env_var_path_data), "data")
        cls.agent_prompts = elvis(os.getenv(env_var_path_prompts), env_var_path_prompts_default)

        return cls._instance

    def get_rel_path_in_data_dir(cls, path_inside_data_dir: str = None) -> str:
        if path_inside_data_dir is None:
            return cls.data_dir
        return cls.data_dir + "." + path_inside_data_dir

    def get_rel_path_in_project_artifacts_dir(cls, project: str, path_inside_project_dir: str = None) -> str:
        if path_inside_project_dir is None:
            return cls.get_rel_path_in_data_dir(project)
        return cls.get_rel_path_in_data_dir(project + "." + path_inside_project_dir)

    def get_path_in_project_artifacts_dir(cls, project: str, path_inside_project_dir: str = None) -> Path:
        pr = cls.get_rel_path_in_project_artifacts_dir(project, path_inside_project_dir)
        root = Paths.get_source_root()
        dir = root / pr.replace(".", "/")
        #dir.mkdir(parents=True, exist_ok=True)
        return dir

    def project_artifact_exists(cls, project: str, path_inside_project_dir: str = None, artifact: str = None) -> bool:
        dir = cls.get_path_in_project_artifacts_dir(project, path_inside_project_dir)
        artifile = dir / artifact
        return artifile.exists()

    def get_project_artifact(cls, project: str, path_inside_project_dir: str = None, artifact: str = None) -> Path:
        dir = cls.get_path_in_project_artifacts_dir(project, path_inside_project_dir)
        artifile = dir / artifact
        return artifile

    def get_agent_history_file(cls, project: str, agent:str) -> Path:
        return cls.get_project_artifact(project, artifact=agent + agent_history_file_suffix)

    @staticmethod
    def get_agent_prompt_file_name(agent:str) -> str:
        return  agent + agent_propmt_file_suffix

    @staticmethod
    def get_file_from_root(path_to_file:str) -> Path:
        return Paths.get_source_root() / path_to_file

    @staticmethod
    def get_source_root() -> Path:
        """Возвращает абсолютный путь до корня проекта."""
        current_dir = Path(__file__).parent
        while True:
            if (current_dir / "pyproject.toml").exists():
                return current_dir
            if current_dir == current_dir.parent:  # Дошли до корня файловой системы
                raise FileNotFoundError("Не удалось найти корень проекта (pyproject.toml не обнаружен)")
            current_dir = current_dir.parent
