import csv
from typing import List, Tuple

from core.stream import Stream
from core.functional import map_validations, partition_validations
from core.validation import Validation
from core.errors import ValidationError
from infrastructure.open_csv import open_csv_file
from core.metrics import compute_metrics, live_progress
from infrastructure.writer import save_valids, save_errors
from validate import (
    validate_date,
    validate_product,
    validate_quantity,
    validate_price,
    validate_customer,
)


# ------------------------
# Validación pura de fila
# ------------------------
def validate_row(row: List[str]) -> Validation[dict, ValidationError]:
    """
    Valida una fila completa del CSV.
    Espera exactamente 6 columnas: date, product, quantity, price, customer, region.
    """
    if len(row) != 6:
        return Validation.failure([
            ValidationError("row", "WRONG_FIELDS", f"Bad row: {row}", row)
        ])

    date, product, quantity, price, customer, region = row

    return map_validations(
        validate_date(date),
        validate_product(product),
        validate_quantity(quantity),
        validate_price(price),
        validate_customer(customer),
        func=lambda d, p, q, pr, c: {
            "date": d,
            "product": p,
            "quantity": q,
            "price": pr,
            "customer": c,
            "region": region,  # se toma directamente del CSV
        }
    )


# ------------------------
# Pipeline principal
# ------------------------
def process(data) -> None:
    """
    Procesa el archivo CSV:
    - Valida cada fila
    - Separa válidas de inválidas
    - Persiste en archivos
    - Muestra progreso y métricas
    """
    reader = csv.reader(data)
    next(reader, None)  # saltar header

    rows: List[Tuple[int, Validation[dict, ValidationError]]] = (
        Stream.from_iterable(enumerate(reader, start=2))
        .map(lambda t: (t[0], validate_row(t[1])))  # (row_index, Validation)
        .tap(lambda t: (
            print(f"✅ Row {t[0]}:", t[1].get_value())
            if t[1].is_success()
            else print(f"❌ Row {t[0]} errors:", t[1].get_errors())
        ))
        .to_list()
    )

    # Separar válidas de errores
    validations = [v for _, v in rows]
    valids, errors = partition_validations(validations)

    # Persistencia
    save_valids(valids)
    save_errors(errors, rows)

    # 📊 Progreso en vivo
    print("\n--- Progreso en vivo ---")
    live_progress(rows)

    # 📊 Métricas finales
    metrics = compute_metrics(rows)
    print("\n--- Métricas finales ---")
    print(f"   Total filas: {metrics['total']}")
    print(f"   Válidas: {metrics['valid']}")
    print(f"   Inválidas: {metrics['invalid']}")
    print(f"   Promedio precio: {metrics['avg_price']:.2f}")

    print(f"\n✅ Saved {len(valids)} valid rows to valid.csv")
    print(f"❌ Saved {len(errors)} errors to errors.csv")


if __name__ == "__main__":
    result = open_csv_file("ventas.csv")
    result.fold(
        on_success=process,
        on_failure=lambda err: print("❌ Error opening CSV:", err),
    )
