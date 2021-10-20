import pytest
from pyformlang.cfg import CFG

from project import cfg_to_wcnf


def is_wcnf(cfg: CFG) -> bool:
    return all(p.is_normal_form() if p.body else True for p in cfg.productions)


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


def test_wcnf(cfg):
    wcnf = cfg_to_wcnf(cfg)
    assert is_wcnf(wcnf)


def test_eps_generation(cfg):
    wcnf = cfg_to_wcnf(cfg)
    if cfg.generate_epsilon():
        assert wcnf.generate_epsilon()
    else:
        assert not wcnf.generate_epsilon()
