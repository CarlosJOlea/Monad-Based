from core.validation import Validation
from core.errors import ValidationError


def is_integer(value: str) -> Validation[int, ValidationError]:
    try:
        return Validation.success(int(value))
    except ValueError:
        return Validation.failure([
            ValidationError(
                column="quantity",
                code="INVALID_INTEGER",
                message=f"Invalid quantity: {value}",
                raw_value=value
            )
        ])


def is_positive(quantity: int) -> Validation[int, ValidationError]:
    if quantity <= 0:
        return Validation.failure([
            ValidationError(
                column="quantity",
                code="NON_POSITIVE",
                message="Quantity must be greater than 0",
                raw_value=quantity
            )
        ])
    return Validation.success(quantity)


def validate_quantity(value: str) -> Validation[int, ValidationError]:
    return is_integer(value).bind(is_positive)
