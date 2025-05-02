# 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

import requests
import json
from src.aice import aice_service2

def test_one():
    txt = aice_service2.generate_command("все скалярные поля персоны и гендера, для персон с гендером мужской")
    print()
    print(txt)
