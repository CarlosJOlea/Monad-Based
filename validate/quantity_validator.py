from core.stream import Stream
from core.validation import Validation
from core.errors import ValidationError

def validate_quantity(value: str) -> Validation[int, ValidationError]:
    def check_integer(v: str):
        try:
            return Validation.success(int(v))
        except ValueError:
            return Validation.failure([
                ValidationError("quantity", "INVALID_INTEGER", f"Invalid quantity: {v}", v)
            ])

    def check_positive(n: int):
        return (Validation.success(n)
            if n > 0 else
            Validation.failure([
                ValidationError("quantity", "NON_POSITIVE", "Must be > 0", n)
            ])
        )

    # pipeline 100% funcional
    return (
        check_integer(value)       # Validation[int]
        .bind(lambda n:            # si fue válido, seguimos
            Stream.from_iterable([check_positive])
            .map(lambda rule: rule(n))  # Stream[Validation[int]]
            .reduce(lambda acc, v: acc if acc.is_failure() else v, Validation.success(n))
        )
    )
