import pytest
from pyformlang.cfg import CFG

from project import cyk


@pytest.mark.parametrize(
    "cfg, words",
    [
        (
            """
                S -> epsilon
                """,
            ["", "epsilon", "abab"],
        ),
        (
            """""",
            ["", "epsilon"],
        ),
        (
            """
                S -> a S b S
                S -> epsilon
                """,
            ["", "aba", "aabbababaaabbb", "abcd", "ab", "aaaabbbb"],
        ),
    ],
)
def test_cyk(cfg, words):
    cfg = CFG.from_text(cfg)
    assert all(cyk(cfg, word) == cfg.contains(word) for word in words)
