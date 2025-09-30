from typing import List, Dict, Callable, Any
from core.validation import Validation
from core.errors import ValidationError

def validate_row_dynamic(
    row: List[str],
    schema: List[tuple[str, Callable[[str], Validation[Any, ValidationError]]]]
) -> Validation[Dict[str, Any], ValidationError]:
    """
    Valida dinámicamente una fila de CSV usando un esquema [(columna, validador)].
    - Cada validador devuelve Validation[valor, ValidationError].
    - Si hay errores, acumula todos en un Validation.failure.
    - Si todo es válido, devuelve un dict {col: valor}.
    """
    if len(row) != len(schema):
        return Validation.failure([
            ValidationError(
                column="row",
                code="WRONG_FIELDS",
                message=f"Expected {len(schema)} fields, got {len(row)}",
                raw_value=row,
            )
        ])

    errors: list[ValidationError] = []
    validated_data: dict[str, Any] = {}

    for (col_name, validator), value in zip(schema, row):
        result = validator(value)
        if result.is_success():
            validated_data[col_name] = result.get_value()
        else:
            errors.extend(result.get_errors())

    if errors:
        return Validation.failure(errors)
    return Validation.success(validated_data)
