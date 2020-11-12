from chuckle_bot import roll

import pytest


@pytest.mark.parametrize(
    "expression,expected",
    [
         ("d20", ["d20"]),
         ("d20+5", ["d20", "+", "5"]),
         ("d20 + 5", ["d20", "+", "5"]),
         ("d20   + 5", ["d20", "+", "5"]),
         ("d20 + 5 - 3d6", ["d20", "+", "5", "-", "3d6"]),
    ])
def test_parse(expression, expected):
    assert expected == roll._parse(expression)


def test_x():
    assert roll.evaluate("d20+2") == 0
