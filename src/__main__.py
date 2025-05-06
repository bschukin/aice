import argparse

from agents.manager import Manager


def main():
    #parser = argparse.ArgumentParser(description="Консольный чат с LLM")
    #parser.add_argument('--load', help="Загрузить историю чата из файла")
    #parser.add_argument('--save', help="Сохранить историю чата в файл")
    #args = parser.parse_args()

    manager = Manager(project="my_console")
    print(f">>> session started with [{manager._history.get_length()}] history messages")

    while True:
        user_input = get_user_input()

        if user_input.lower() in ['e', 'exit', 'quit', 'q', 'й']:
            manager.dump_state()
            break

        if user_input.lower() in ['0', 'o']:
            manager.reset_state()
            continue

        if user_input.lower() in ['1']:
            manager.dump_state()
            continue

        print(manager.chat(user_input))


def get_user_input(prompt="aice>>"):
    return input(prompt)

if __name__ == "__main__":
    main()