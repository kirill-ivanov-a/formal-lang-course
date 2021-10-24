import pytest

from pyformlang.cfg import Production, Variable, Terminal
from project import cfg_from_file


@pytest.mark.parametrize(
    "text_cfg",
    ["""""", """A -> b"""],
)
def test_empty_cfg(tmpdir, text_cfg):
    file = tmpdir.mkdir("test_dir").join("cfg")
    file.write(text_cfg)
    cfg = cfg_from_file(file)

    assert cfg.is_empty()


@pytest.mark.parametrize(
    "text_cfg, expected_productions",
    [
        ("""""", set()),
        ("""A -> b""", {Production(Variable("A"), [Terminal("b")])}),
        (
            """
        S -> epsilon
        S -> a S b
        S -> S S
        """,
            {
                Production(Variable("S"), []),
                Production(
                    Variable("S"), [Terminal("a"), Variable("S"), Terminal("b")]
                ),
                Production(Variable("S"), [Variable("S"), Variable("S")]),
            },
        ),
    ],
)
def test_productions(tmpdir, text_cfg, expected_productions):
    file = tmpdir.mkdir("test_dir").join("cfg")
    file.write(text_cfg)
    cfg = cfg_from_file(file)
    actual_productions = cfg.productions

    assert actual_productions == expected_productions
