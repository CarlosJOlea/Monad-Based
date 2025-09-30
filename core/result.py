from typing import Callable, Generic, TypeVar, Union
from enum import Enum

T = TypeVar("T")
E = TypeVar("E")


class ResultType(Enum):
    SUCCESS = 1
    FAILURE = 2


class Result(Generic[T, E]):
    """
    Monad for operations that may fail and should short-circuit on first error.
    """

    def __init__(self, result_type: ResultType, value: T = None, error: E = None):
        self.result_type = result_type
        self._value = value
        self._error = error

    @classmethod
    def success(cls, value: T) -> "Result[T, E]":
        return cls(ResultType.SUCCESS, value=value)

    @classmethod
    def failure(cls, error: E) -> "Result[T, E]":
        return cls(ResultType.FAILURE, error=error)

    def is_success(self) -> bool:
        return self.result_type == ResultType.SUCCESS

    def is_failure(self) -> bool:
        return self.result_type == ResultType.FAILURE

    def map(self, func: Callable[[T], T]) -> "Result[T, E]":
        if self.is_success():
            try:
                return Result.success(func(self._value))
            except Exception as e:
                return Result.failure(str(e))
        return self

    def bind(self, func: Callable[[T], "Result[T, E]"]) -> "Result[T, E]":
        if self.is_success():
            try:
                return func(self._value)
            except Exception as e:
                return Result.failure(str(e))
        return self

    def fold(self, on_success: Callable[[T], T], on_failure: Callable[[E], T]) -> T:
        return on_success(self._value) if self.is_success() else on_failure(self._error)

    def get_or_else(self, default: T) -> T:
        return self._value if self.is_success() else default

    def get_value(self) -> Union[T, None]:
        return self._value if self.is_success() else None

    def get_error(self) -> Union[E, None]:
        return self._error if self.is_failure() else None
