from src.utils.FileUtils import write_file, read_file, write_project_file, read_project_file
from src.llm.message_history import MessageHistory

def test_substring():
    text = "Hello, worldd"
    text = text[0:-1]
    assert text == "Hello, world"

