from typing import Callable, TypeVar, List, Tuple
from core.validation import Validation
from functools import wraps

# Type variables
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")
R = TypeVar("R")
T = TypeVar("T")


def lift(func: Callable[..., R]) -> Callable[..., Validation[R, E]]:
    """
    Eleva una función normal a una función que trabaja sobre Validation.
    """
    @wraps(func)
    def wrapper(*validations: Validation) -> Validation[R, E]:
        if all(v.is_success() for v in validations):
            values = [v.get_value() for v in validations]
            return Validation.success(func(*values))
        errors = []
        for v in validations:
            if not v.is_success():
                errors.extend(v.get_errors())
        return Validation.failure(errors)
    return wrapper

def map_validations(*validations: Validation, func: Callable[..., R]) -> Validation[R, E]:
    return lift(func)(*validations)

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

def partition_validations(validations: List[Validation[T, E]]) -> Tuple[List[T], List[E]]:
    valids: List[T] = []
    errors: List[E] = []
    for v in validations:
        if v.is_success():
            valids.append(v.get_value())
        else:
            errors.extend(v.get_errors())
    return valids, errors
