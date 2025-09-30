from typing import Callable, TypeVar, List, Tuple
from core.validation import Validation

# Type variables
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
F = TypeVar("F")
R = TypeVar("R")
E = TypeVar("E")
T = TypeVar("T")


# -----------------------
# Lift combinators
# -----------------------
def lift(func: Callable[[A], B]) -> Callable[[Validation[A, E]], Validation[B, E]]:
    return lambda v: v.map(func)


def lift2(func: Callable[[A, B], C]):
    return lambda v1, v2: (
        Validation.success(func(v1.get_value(), v2.get_value()))
        if v1.is_success() and v2.is_success()
        else Validation.failure(v1.get_errors() + v2.get_errors())
    )


def lift3(func: Callable[[A, B, C], R]):
    return lambda v1, v2, v3: (
        Validation.success(func(v1.get_value(), v2.get_value(), v3.get_value()))
        if v1.is_success() and v2.is_success() and v3.is_success()
        else Validation.failure(v1.get_errors() + v2.get_errors() + v3.get_errors())
    )


def lift4(func: Callable[[A, B, C, D], R]):
    return lambda v1, v2, v3, v4: (
        Validation.success(func(v1.get_value(), v2.get_value(), v3.get_value(), v4.get_value()))
        if all(v.is_success() for v in [v1, v2, v3, v4])
        else Validation.failure(v1.get_errors() + v2.get_errors() + v3.get_errors() + v4.get_errors())
    )


# -----------------------
# Map combinators
# -----------------------
def map2(v1, v2, func):
    return lift2(func)(v1, v2)


def map3(v1, v2, v3, func):
    return lift3(func)(v1, v2, v3)


def map4(v1, v2, v3, v4, func):
    return lift4(func)(v1, v2, v3, v4)


def map5(v1, v2, v3, v4, v5, func):
    return sequence_validations([v1, v2, v3, v4, v5]).map(
        lambda vs: func(*vs)
    )


# -----------------------
# Traversal
# -----------------------
def sequence_validations(validations: List[Validation[T, E]]) -> Validation[List[T], E]:
    values: List[T] = []
    errors: List[E] = []
    for v in validations:
        if v.is_success():
            values.append(v.get_value())
        else:
            errors.extend(v.get_errors())
    return Validation.success(values) if not errors else Validation.failure(errors)


def traverse_validations(values: List[A], func: Callable[[A], Validation[B, E]]) -> Validation[List[B], E]:
    return sequence_validations([func(v) for v in values])


# -----------------------
# Partition
# -----------------------
def partition_validations(validations: List[Validation[T, E]]) -> Tuple[List[T], List[E]]:
    valids: List[T] = []
    errors: List[E] = []
    for v in validations:
        if v.is_success():
            valids.append(v.get_value())
        else:
            errors.extend(v.get_errors())
    return valids, errors
