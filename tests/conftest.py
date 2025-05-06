import pytest
from dotenv import load_dotenv
from pathlib import Path

@pytest.fixture(autouse=True, scope="session")
def load_env():
    env_path = Path(__file__).parent.parent/ ".env.test"

    print(env_path)
    load_dotenv(env_path, override=True)