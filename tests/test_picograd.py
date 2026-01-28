import pytest

from ai_tower.picograd.node import Node


def test_simple_eq():
    a = Node(.2)
    b = Node(.4)
    y = a + b

    assert y.value == pytest.approx(a.value + b.value)
