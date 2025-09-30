from core.validation import Validation
from core.errors import ValidationError


def is_float(value: str) -> Validation[float, ValidationError]:
    try:
        return Validation.success(float(value))
    except ValueError:
        return Validation.failure([
            ValidationError(
                column="price",
                code="INVALID_NUMBER",
                message=f"Invalid price: {value}",
                raw_value=value
            )
        ])


def is_non_negative(price: float) -> Validation[float, ValidationError]:
    if price < 0:
        return Validation.failure([
            ValidationError(
                column="price",
                code="NEGATIVE",
                message="Price cannot be negative",
                raw_value=price
            )
        ])
    return Validation.success(price)


def validate_price(value: str) -> Validation[float, ValidationError]:
    return is_float(value).bind(is_non_negative)
