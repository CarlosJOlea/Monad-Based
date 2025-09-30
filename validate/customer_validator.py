from core.validation import Validation
from core.errors import ValidationError


def not_empty(value: str) -> Validation[str, ValidationError]:
    if not value or not value.strip():
        return Validation.failure([
            ValidationError(
                column="customer",
                code="EMPTY",
                message="Customer cannot be empty",
                raw_value=value
            )
        ])
    return Validation.success(value)


def strip_value(value: str) -> Validation[str, ValidationError]:
    # Aquí no validamos, solo transformamos con map
    return Validation.success(value.strip())


def validate_customer(value: str) -> Validation[str, ValidationError]:
    return not_empty(value).bind(strip_value)
