from sqlalchemy.testing.plugin.plugin_base import start_test_class_outside_fixtures

from pushkin.Pushkin import Pushkin
from pushkin.prompts.pushkin_response import ChangeItem, AiAgentResponse
import re

from utils.md import buildMDTree, apply_md_changes


def test_md_build_print():
    md = """
кукареку

# Раздел1
  Привет

# Раздел2
  Сосед
# Раздел4
## Раздел41
  Иваново
## Раздел42
  Москва
    """
    mdtree = buildMDTree(md)
    print(mdtree.getMDText())
    assert clean(mdtree.getMDText())==clean(md)


def test_md_change():
    md = """
# Кукареку

# Раздел1
  Привет

# Раздел2
  Сосед
# Раздел4
## Раздел41
  Иваново
## Раздел42
  Москва
    """.strip()
    print("=============")
    pr = AiAgentResponse(for_human="", changes_made=[], conflicts=[], requires_confirmation=False, full_document=None)
    pr.changes_made.append(ChangeItem(type="add", sections=["Раздел4", "Раздел43"], new_text="Кохма", old_text=None))
    text = apply_md_changes(md, pr)
    print(text)


def test_md_read():
    p = Pushkin()
    md = p.get_STD()
    tree = buildMDTree(md)

    print(tree.getMDText())


def clean(s:str)->str:
    return (re.sub(r"[^a-zA-Z0-9а-яА-ЯёЁ]", "",s)
            .lower())
