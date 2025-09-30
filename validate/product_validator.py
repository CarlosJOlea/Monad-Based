from core.validation import Validation
from core.errors import ValidationError

def validate_product(value: str) -> Validation[str, ValidationError]:
    if not value.strip():
        return Validation.failure([
            ValidationError("product", "EMPTY", "Product cannot be empty", value)
        ])
    return Validation.success(value.strip())
