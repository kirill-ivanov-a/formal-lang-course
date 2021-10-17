import pytest
from pyformlang.cfg import CFG

from project import cfg_to_cnf


@pytest.fixture(
    params=[
        """
    """,
        """
    N -> A B
    """,
        """
    S -> epsilon
    S -> a S b
    S -> S S
    """,
        """
    S -> epsilon
    S -> a S b S
    """,
    ]
)
def cfg(request):
    return CFG.from_text(request.param)


def test_cnf(cfg):
    cnf = cfg_to_cnf(cfg)
    assert cnf.is_normal_form()
