from src.utils.file_io import write_file, read_file, write_project_file, read_project_file
from agents.message_history import MessageHistory

def test_fileutils_rw():
    text = "Hello, worldina"
    write_file("data.test", "testw01.txt", text)
    textr = read_file("data.test", "testw01.txt")
    assert textr==text

def test_fileutils_project_rw():
    text = "Hello, wordina"
    write_project_file("test", "testw02.txt", text)
    textr = read_project_file("test", "testw02.txt")
    assert textr==text

def test_chathistory_rw():
    cs = MessageHistory("project1", "manager")
    cs.delete_all_history()
    cs.add_message("xxx", "hw")
    cs.add_message("xxx2", "hw2")
    cs.dump_to_file()

    cs2 = MessageHistory("project1", "manager")
    print(cs2.get_full_messages())
    assert(len(cs2.messages)==2)