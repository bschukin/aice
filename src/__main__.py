import argparse

from agents.analyst import Analyst
from agents.manager import Manager


def main():
    #parser = argparse.ArgumentParser(description="Консольный чат с LLM")
    #parser.add_argument('--load', help="Загрузить историю чата из файла")
    #parser.add_argument('--save', help="Сохранить историю чата в файл")
    #args = parser.parse_args()

    agent = Analyst(project="starter")
    print(f">>> session started with:")
    print(f">>> \t\tthe agent role [{agent.role}]")
    print(f">>> \t\t[{agent._history.get_length()}] history messages")

    while True:
        user_input = get_user_input()

        if user_input.lower() in ['e', 'exit', 'quit', 'q', 'й']:
            agent.dump_state()
            break

        if user_input.lower() in ['0', 'o']:
            agent.reset_state()
            continue

        if user_input.lower() in ['1']:
            agent.dump_state()
            continue
        print("...")
        print(agent.chat(user_input))


def get_user_input(prompt="aice>>"):
    return input(prompt)

if __name__ == "__main__":
    main()