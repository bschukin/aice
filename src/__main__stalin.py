import traceback

from stalin.Stalin import Stalin
from utils.md import print_markdown


def main():
    # parser = argparse.ArgumentParser(description="Консольный чат с LLM")
    # parser.add_argument('--load', help="Загрузить историю чата из файла")
    # parser.add_argument('--save', help="Сохранить историю чата в файл")
    # args = parser.parse_args()

    stalin = Stalin()
    print(f">>> session started with:")
    print(f">>> \t\tthe agent role [{stalin.role}]")
    print(f">>> \t\t[{stalin._history.get_length()}] history messages")

    while True:
        user_input = get_user_input()

        if user_input.lower() in ['e', 'exit', 'quit', 'q', 'й']:
            stalin.dump_state()
            break

        if user_input.lower() in ['0', 'o']:
            stalin.reset_state()
            continue

        if user_input.lower() in ['1']:
            stalin.dump_state()
            continue
        print("...")
        try:
            resp = stalin.chat(user_input)
            print_markdown(resp)
        except Exception as e:
            traceback.print_exc()
            print(f"Ошибка: {str(e)}")
        pass
    # resp_parsed = pushkin.parse_agent_response(resp)



def get_user_input(prompt="stalin>>"):
    return input(prompt)


if __name__ == "__main__":
    main()
