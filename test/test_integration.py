import csv
import os
from infrastructure.open_csv import open_csv_file
from examples.main import validate_row, save_valids, save_errors
from core.functional import partition_validations
from core.metrics import compute_metrics
from core.stream import Stream

def test_integration_pipeline(tmp_path):
    # --- Arrange ---
    sample_csv = tmp_path / "ventas.csv"
    sample_csv.write_text(
        "date,product,quantity,price,customer\n"
        "2025-09-01,Widget A,2,60.0,Cliente 1\n"
        "2025-09-02,Widget B,1,120,Cliente 2\n"
        ",Widget C,3,50,Cliente 3\n"
        "2025-09-03,Widget D,abc,20,Cliente 4\n"
    )

    result = open_csv_file(str(sample_csv))

    def process(data):
        reader = csv.reader(data)
        next(reader)

        rows = (
            Stream.from_iterable(enumerate(reader, start=2))
            .map(lambda t: (t[0], validate_row(t[1])))
            .to_list()
        )

        validations = [v for _, v in rows]
        valids, errors = partition_validations(validations)

        # --- Persistencia ---
        valid_csv = tmp_path / "valid.csv"
        error_csv = tmp_path / "errors.csv"
        save_valids(valids, str(valid_csv))
        save_errors(errors, rows, str(error_csv))

        # --- Métricas ---
        metrics = compute_metrics(rows)

        # --- Assert ---
        assert metrics["total"] == 4
        assert metrics["valid"] == 2
        assert metrics["invalid"] == 2
        assert valid_csv.exists()
        assert error_csv.exists()

    result.fold(
        on_success=process,
        on_failure=lambda err: (_ for _ in ()).throw(Exception(err))
    )
