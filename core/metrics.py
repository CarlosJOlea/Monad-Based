from core.stream import Stream

# Función pura: acumular progreso
def accumulate_progress(acc, t):
    return {
        "total": acc["total"] + 1,
        "valid": acc["valid"] + (1 if t[1].is_success() else 0),
        "invalid": acc["invalid"] + (1 if t[1].is_failure() else 0),
    }


def live_progress(rows):
    return (
        Stream.from_iterable(rows)
        .scan(accumulate_progress, {"total": 0, "valid": 0, "invalid": 0})
        .to_list()
    )
    # 👉 Quien consuma live_progress decide si imprime o no.


# Función pura: acumular métricas
def accumulate_metrics(acc, t):
    return {
        "total": acc["total"] + 1,
        "valid": acc["valid"] + (1 if t[1].is_success() else 0),
        "invalid": acc["invalid"] + (1 if t[1].is_failure() else 0),
        "sum_price": acc["sum_price"] + (
            t[1].get_value()["price"] if t[1].is_success() else 0
        ),
    }


def compute_metrics(rows):
    acc = (
        Stream.from_iterable(rows)
        .reduce(accumulate_metrics, {"total": 0, "valid": 0, "invalid": 0, "sum_price": 0.0})
    )
    return {
        **acc,
        "avg_price": acc["sum_price"] / acc["valid"] if acc["valid"] > 0 else 0,
    }
