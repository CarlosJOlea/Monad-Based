from core.stream import Stream
from core.validation import Validation
from core.errors import ValidationError

def validate_quantity(value: str) -> Validation[int, ValidationError]:
    # --- Reglas de formato ---
    def check_integer(v: str):
        try:
            n = int(v)
            return [], n  # sin errores, devuelve el valor convertido
        except ValueError:
            return [ValidationError("quantity", "INVALID_INTEGER", f"Invalid quantity: {v}", v)], None

    # --- Reglas de negocio (requieren el int) ---
    def check_positive(n: int):
        return [] if n > 0 else [
            ValidationError("quantity", "NON_POSITIVE", "Must be > 0", n)
        ]

    # 1. Corremos las reglas de formato
    int_errors, parsed = check_integer(value)
    if int_errors:
        return Validation.failure(int_errors)

    # 2. Corremos las reglas de negocio con Stream
    errors = (
        Stream.from_iterable([check_positive])
        .flat_map(lambda rule: rule(parsed))  # ya es seguro, parsed es int
        .to_list()
    )

    return (
        Validation.failure(errors) if errors
        else Validation.success(parsed)
    )
