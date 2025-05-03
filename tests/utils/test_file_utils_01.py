from src.utils.FileUtils import write_file, read_file, write_project_file, read_project_file

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