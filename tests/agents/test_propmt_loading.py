from paths import Paths
from src.agents.system_prompt import SystemPrompt
from utils.md import print_markdown


def test_load_system_prompt_including_common_part():
    print()
    """
    тест на загрузку системного промпта c включением отдельных общих для команды частей промпта
    """

    sp = SystemPrompt(agent_name="manager2", project="test01")
    print_markdown(sp.agent_prompt)

def test_load_system_prompt():
    print()
    """
    тест на загрузку системного промпта из разных источников
    """

    assert Paths().data_dir=="tests.data"
    assert Paths().get_rel_path_in_data_dir() == "tests.data"
    assert Paths().get_rel_path_in_data_dir("some_project") == "tests.data.some_project"
    assert Paths().get_rel_path_in_project_artifacts_dir("some_project") == "tests.data.some_project"


    sp = SystemPrompt(agent_name="namager", project="test01")
    assert sp.agent_prompt=="Ты - сообразительный и остроумный ассистент-помощник"

    sp = SystemPrompt(agent_name="manager", project="test01")
    assert sp.agent_prompt == "Ты - сообразительный и остроумный ассистент-дурак"

    assert sp.prd_schema is not None
    assert sp.response_schema is not None
    print_markdown(sp.response_schema)
