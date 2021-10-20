import pytest
from pyformlang.cfg import CFG

from project import cfg_to_wcnf


def is_wcnf(cfg: CFG) -> bool:
    return all(p.is_normal_form() if p.body else True for p in cfg.productions)


def get_eps_generating_vars(cfg: CFG) -> set:
    return {p.head.value for p in cfg.productions if not p.body}


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
        """
        A -> epsilon
        B -> epsilon
        C -> epsilon
    """,
    ]
)
def cfg(request):
    return CFG.from_text(request.param)


def test_wcnf(cfg):
    wcnf = cfg_to_wcnf(cfg)
    assert is_wcnf(wcnf)


@pytest.mark.parametrize(
    "cfg, exp_eps_gen_vars",
    [
        (
            """
        S -> S S | epsilon
        """,
            {"S"},
        ),
        (
            """
        S -> S S | A
        A -> B | epsilon
        B -> epsilon
        """,
            {"S"},
        ),
        (
            """
        S -> A a | S a
        A -> epsilon
        B -> epsilon
        """,
            {"A"},
        ),
    ],
)
def test_eps_generating(cfg, exp_eps_gen_vars):
    wcnf = cfg_to_wcnf(CFG.from_text(cfg))
    act_eps_gen_vars = get_eps_generating_vars(wcnf)
    assert act_eps_gen_vars == exp_eps_gen_vars
