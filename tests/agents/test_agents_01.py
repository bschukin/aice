from agents.analyst import Analyst
from src.agents.manager import Manager
from src.agents.architect import Architect


def test_000_whoamai():
    mgr = Manager()
    assert mgr.role=="manager"
    assert mgr.name == "Babalyan"

    mgr = Manager("Борис")
    assert mgr.role == "manager"
    assert mgr.name == "Борис"

    arch = Architect()
    assert arch.role == "architect"
    assert arch.name == "Vikulin"

def test_001_parse_human_responce():
    a = Analyst()
    a.reset_state()
    print(a.chat("Мы делаем проект посвященный моей домашней библиотеке."
                 "В библиотеке есть книги. Каждая книга имеет несколько авторов."
                 "У каждой книги может быть несколько изданий. Издание имеет атрибуты - год издания, тираж."))
    print(a.chat("Зачем ты добавил системное требование в PRD, ведь я не просил его добавить? "))
    a.dump_state()

