from dataclasses import dataclass
from typing import Any


@dataclass
class ValidationError:
    column: str
    code: str
    message: str
    raw_value: Any
    row_index: int | None = None
