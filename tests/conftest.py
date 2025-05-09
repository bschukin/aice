import pytest
from dotenv import load_dotenv
from pathlib import Path
from loguru import logger
import sys

@pytest.fixture(autouse=True, scope="session")
def load_env():
    env_path = Path(__file__).parent.parent/ ".env.test"

    print(env_path)
    load_dotenv(env_path, override=True)

    logger.remove()

    # Добавляем обработчик с ЖЁСТКО заданным уровнем WARN
    logger.add(
        sink=sys.stdout,
        format="{time:HH:mm:ss} {level: <5}| {file}:{line} | {message}",
        level="INFO",
        colorize=False
    )