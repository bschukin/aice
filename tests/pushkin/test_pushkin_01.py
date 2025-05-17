from pushkin.Pushkin import Pushkin


def test_pushkin_prompt():
    p = Pushkin()
    prompt = p._get_system_prompt()

    for item in prompt:
        print(item)

    assert prompt[1]['content'].lower().__contains__("по имени Пушкин".lower())

def test_pushkin_chat():
    p = Pushkin()
    p.reset_state()
    res = p.chat("Привет, Пушкин! Внеси главную задачу в 25й: сделаться экспертом в разработке ИИ-агентов")
    print(res)
    #p.parse_agent_response(res)
    #print(p.chat("Мультики я просмотрел. Добавь в список дел покурить. и выведи список в формате md"))
    #print(p.chat("Промпт написан. обнови список"))