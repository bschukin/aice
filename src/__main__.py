import argparse

from agents.analyst import Analyst
from agents.manager import Manager
from pushkin.Pushkin import Pushkin
from utils.md import print_markdown


def main():
    #parser = argparse.ArgumentParser(description="Консольный чат с LLM")
    #parser.add_argument('--load', help="Загрузить историю чата из файла")
    #parser.add_argument('--save', help="Сохранить историю чата в файл")
    #args = parser.parse_args()

    pushkin = Pushkin()
    print(f">>> session started with:")
    print(f">>> \t\tthe agent role [{pushkin.role}]")
    print(f">>> \t\t[{pushkin._history.get_length()}] history messages")

    while True:
        user_input = get_user_input()

        if user_input.lower() in ['e', 'exit', 'quit', 'q', 'й']:
            pushkin.dump_state()
            break

        if user_input.lower() in ['0', 'o']:
            pushkin.reset_state()
            continue

        if user_input.lower() in ['1']:
            pushkin.dump_state()
            continue
        print("...")
        resp = pushkin.chat(user_input)
        resp_parsed = pushkin.parse_agent_response(resp)
        print_markdown(resp_parsed)


def get_user_input(prompt="aice>>"):
    return input(prompt)

if __name__ == "__main__":
    main()