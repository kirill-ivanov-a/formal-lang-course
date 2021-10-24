import pytest

from project import ecfg_to_rsm, ECFG, Box, regex_to_min_dfa


@pytest.mark.parametrize(
    """ecfg_text""",
    (
        """
        """,
        """
        S -> $
        """,
        """
        S -> a S b S
        B -> B B
        C -> A B C
        """,
    ),
)
def test_boxes_regex_equality(ecfg_text):
    ecfg = ECFG.from_text(ecfg_text)
    rsm = ecfg_to_rsm(ecfg)
    act_start_symbol = ecfg.start_symbol
    exp_start_symbol = rsm.start_symbol
    exp_boxes = [Box(p.head, regex_to_min_dfa(p.body)) for p in ecfg.productions]
    act_boxes = rsm.boxes
    return act_start_symbol == exp_start_symbol and act_boxes == exp_boxes
