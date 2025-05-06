from src.agents.manager import Manager
from src.agents.architect import Architect


def test_000_whoamai():
    mgr = Manager()
    assert mgr.role=="manager"
    assert mgr.name == "Babalyan"

    mgr = Manager("Борис")
    assert mgr.role == "manager"
    assert mgr.name == "Борис"

    arch = Architect()
    assert arch.role == "architect"
    assert arch.name == "Vikulin"



