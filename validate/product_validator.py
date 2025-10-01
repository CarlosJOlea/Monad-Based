from core.stream import Stream
from core.validation import Validation
from core.errors import ValidationError

def validate_product(value: str) -> Validation[str, ValidationError]:
    rules = [
        lambda v: v.strip() != "",
        lambda v: not v.strip().isdigit(),  # ejemplo: no puro número
    ]

    errors = (
        Stream.from_iterable(rules)                     # stream de reglas
        .filter(lambda rule: not rule(value))           # filtra las que fallan
        .map(lambda _: ValidationError(
            column="product",
            code="INVALID",
            message=f"Invalid product: {value}",
            raw_value=value
        ))
        .to_list()
    )

    return (
        Validation.failure(errors) if errors
        else Validation.success(value.strip())
    )
