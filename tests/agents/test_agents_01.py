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
    print(a.chat("Ок. Продолжим. Добавь системное требование: Должен быть логин и пароль для входа в систему"))
    print(a.chat("Пароль должен иметь не более 12 символов в длину. Автор может иметь атрибуты фото, биография"))
    #print(a.chat("Система должна обслуживать до 50 пользователей, в качестве сервера служит макбук аир"))
    a.dump_state()

