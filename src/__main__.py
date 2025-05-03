import argparse

from agents.Manager import Manager


def main():
    #parser = argparse.ArgumentParser(description="Консольный чат с LLM")
    #parser.add_argument('--load', help="Загрузить историю чата из файла")
    #parser.add_argument('--save', help="Сохранить историю чата в файл")
    #args = parser.parse_args()

    m = Manager()

    while True:
        user_input = get_user_input()

        if user_input.lower() in ['e', 'exit', 'quit', 'q']:
            break

        print(m.chat(user_input))

def get_user_input(prompt="aice>> "):
    return input(prompt)

if __name__ == "__main__":
    main()