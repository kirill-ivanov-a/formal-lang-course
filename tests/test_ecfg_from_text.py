import pytest

from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

from project import ECFG, regex_to_min_dfa, InvalidECFGFormatException


def check_regex_equality(r1: Regex, r2: Regex):
    return regex_to_min_dfa(r1).is_equivalent_to(regex_to_min_dfa(r2))


@pytest.mark.parametrize(
    "text_ecfg, expected_productions",
    [
        ("""""", []),
        (
            """S -> a S b S | $""",
            {
                Variable("S"): Regex("a S b S | $"),
            },
        ),
        ("""S -> (a | b)* c""", {Variable("S"): Regex("(a | b)* c")}),
        (
            """
         S -> (a (S | $) b)*
         A -> a b c
         """,
            {
                Variable("S"): Regex("(a (S | $) b)*"),
                Variable("A"): Regex("a b c"),
            },
        ),
    ],
)
def test_read_from_text(text_ecfg, expected_productions):
    ecfg = ECFG.from_text(text_ecfg)
    assert len(ecfg.productions) == len(expected_productions) and all(
        check_regex_equality(p.body, expected_productions[p.head])
        for p in ecfg.productions
    )


@pytest.mark.parametrize(
    "text_cfg",
    [
        """S -> B -> C""",
        """A -> b B -> a""",
        """
        S -> a S b S
        A -> B ->
        """,
    ],
)
def test_more_than_one_production_per_line(text_cfg):
    with pytest.raises(InvalidECFGFormatException):
        ECFG.from_text(text_cfg)


@pytest.mark.parametrize(
    "text_cfg",
    [
        """
        S -> B
        S -> A
        """,
        """
        A -> b
        B -> a
        A -> c""",
    ],
)
def test_more_than_one_production_with_line(text_cfg):
    with pytest.raises(InvalidECFGFormatException):
        ECFG.from_text(text_cfg)
