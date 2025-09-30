import pytest
from core.validation import Validation

# ---------- Functor Laws ----------
def test_functor_identity():
    v = Validation.success(42)
    assert v.map(lambda x: x).get_value() == v.get_value()

def test_functor_composition():
    f = lambda x: x + 1
    g = lambda x: x * 2
    v = Validation.success(10)
    left = v.map(lambda x: f(g(x)))
    right = v.map(g).map(f)
    assert left.get_value() == right.get_value()

# ---------- Monad Laws ----------
def test_monad_left_identity():
    f = lambda x: Validation.success(x + 1)
    a = 5
    left = Validation.success(a).bind(f)
    right = f(a)
    assert left.get_value() == right.get_value()

def test_monad_right_identity():
    v = Validation.success(7)
    left = v.bind(Validation.success)
    assert left.get_value() == v.get_value()

def test_monad_associativity():
    f = lambda x: Validation.success(x + 1)
    g = lambda x: Validation.success(x * 2)
    v = Validation.success(3)
    left = v.bind(f).bind(g)
    right = v.bind(lambda x: f(x).bind(g))
    assert left.get_value() == right.get_value()
