import datetime
from core.validation import Validation
from core.errors import ValidationError


def not_empty(value: str) -> Validation[str, ValidationError]:
    return Validation.failure([
        ValidationError("date", "EMPTY", "Date cannot be empty", value)
    ]) if not value or not value.strip() else Validation.success(value)

def is_date_format(value: str) -> Validation[str, ValidationError]:
    try:
        datetime.datetime.strptime(value, "%Y-%m-%d")
        return Validation.success(value)
    except ValueError:
        return Validation.failure([
            ValidationError("date", "INVALID_FORMAT", f"Invalid date: {value}", value)
        ])

def validate_date(value: str) -> Validation[str, ValidationError]:
    return not_empty(value).bind(is_date_format)
