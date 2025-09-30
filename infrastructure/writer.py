# infrastructure/writer.py
import csv
from typing import Iterable, Sequence
from core.errors import ValidationError

FIELDNAMES = ["date", "product", "quantity", "price", "customer","region"]

def save_valids(valids: Sequence[dict], path: str = "valid.csv") -> None:
    with open(path, "w", encoding="utf-8", newline="") as vf:
        w = csv.DictWriter(vf, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(valids)

def save_errors(
    _errors: Sequence[ValidationError],  # compat param
    indexed_rows: Iterable[tuple[int, object]],
    path: str = "errors.csv",
) -> None:
    with open(path, "w", encoding="utf-8", newline="") as ef:
        w = csv.writer(ef)
        w.writerow(["row_index", "column", "code", "message", "raw_value"])
        for (row_idx, v) in indexed_rows:
            if hasattr(v, "is_failure") and v.is_failure():
                for e in v.get_errors():
                    w.writerow([row_idx, e.column, e.code, e.message, e.raw_value])
