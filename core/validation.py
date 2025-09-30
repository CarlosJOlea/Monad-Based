from typing import Callable, Generic, TypeVar, List
from infrastructure.open_csv import open_csv_file

T = TypeVar("T")
E = TypeVar("E")


class Validation(Generic[T, E]):
    """
    Applicative Validation:
    - Accumulates errors (list[E]) instead of short-circuiting.
    - Use for validating independent fields in parallel.
    """

    def __init__(self, value: T = None, errors: List[E] = None):
        self._value = value
        self._errors = errors or []

    @classmethod
    def success(cls, value: T) -> "Validation[T, E]":
        return cls(value=value)

    @classmethod
    def failure(cls, errors: List[E]) -> "Validation[T, E]":
        return cls(errors=errors)

    def is_success(self) -> bool:
        return not self._errors

    def is_failure(self) -> bool:
        return bool(self._errors)

    def map(self, func: Callable[[T], T]) -> "Validation[T, E]":
        if self.is_success():
            try:
                return Validation.success(func(self._value))
            except Exception as e:
                return Validation.failure([str(e)])
        return self

    def apply(self, other: "Validation[Callable[[T], T], E]") -> "Validation[T, E]":
        if self.is_success() and other.is_success():
            return Validation.success(other._value(self._value))
        else:
            return Validation.failure(self._errors + other._errors)

    def bind(self, func: Callable[[T], "Validation[T, E]"]) -> "Validation[T, E]":
        """
        Monad-like bind: chain computations that return Validation.
        If already invalid, propagate the errors.
        """
        if self.is_success():
            try:
                return func(self._value)
            except Exception as e:
                return Validation.failure([str(e)])
        return self

    def get_value(self) -> T:
        return self._value if self.is_success() else None

    def get_errors(self) -> List[E]:
        return self._errors
