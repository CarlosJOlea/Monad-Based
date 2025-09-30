from core.stream import Stream

def live_progress(rows):
    (
        Stream.from_iterable(rows)
        .scan(
            lambda acc, t: {
                "total": acc["total"] + 1,
                "valid": acc["valid"] + (1 if t[1].is_success() else 0),
                "invalid": acc["invalid"] + (1 if t[1].is_failure() else 0),
            },
            {"total": 0, "valid": 0, "invalid": 0},
        )
        .tap(lambda m: print("📈 Progreso:", m))
        .to_list()
    )


def compute_metrics(rows):
    acc = (
        Stream.from_iterable(rows)
        .reduce(
            lambda acc, t: {
                "total": acc["total"] + 1,
                "valid": acc["valid"] + (1 if t[1].is_success() else 0),
                "invalid": acc["invalid"] + (1 if t[1].is_failure() else 0),
                "sum_price": acc["sum_price"] + (
                    t[1].get_value()["price"] if t[1].is_success() else 0
                ),
            },
            {"total": 0, "valid": 0, "invalid": 0, "sum_price": 0.0},
        )
    )

    # ya es un dict final, solo ajustamos
    acc["avg_price"] = acc["sum_price"] / acc["valid"] if acc["valid"] > 0 else 0
    return acc
