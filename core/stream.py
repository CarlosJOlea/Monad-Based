from typing import Callable, Generic, Iterable, Iterator, List, TypeVar

T = TypeVar("T")
U = TypeVar("U")
A = TypeVar("A")
B = TypeVar("B")


class Stream(Generic[T]):
    """
    Stream síncrono funcional.
    Permite componer pipelines de datos usando map, filter, tap, scan, reduce, etc.
    """

    def __init__(self, source: Iterable[T]):
        self.source = source

    # -----------------------
    # Fuentes (sources)
    # -----------------------
    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> "Stream[T]":
        return cls(iterable)

    @classmethod
    def from_generator(cls, gen_func: Callable[[], Iterator[T]]) -> "Stream[T]":
        return cls(gen_func())

    # -----------------------
    # Transformaciones
    # -----------------------
    def map(self, func: Callable[[T], U]) -> "Stream[U]":
        return Stream(func(x) for x in self.source)

    def filter(self, predicate: Callable[[T], bool]) -> "Stream[T]":
        return Stream(x for x in self.source if predicate(x))

    def flat_map(self, func: Callable[[T], Iterable[U]]) -> "Stream[U]":
        return Stream(y for x in self.source for y in func(x))

    # -----------------------
    # Side-effects
    # -----------------------
    def tap(self, func: Callable[[T], None]) -> "Stream[T]":
        def generator():
            for x in self.source:
                func(x)  # efecto controlado (log/print/metricas)
                yield x
        return Stream(generator())

    # -----------------------
    # Acumuladores
    # -----------------------
    def scan(self, func: Callable[[A, T], A], initial: A) -> "Stream[A]":
        def generator():
            acc = initial
            for x in self.source:
                acc = func(acc, x)
                yield acc
        return Stream(generator())

    def reduce(self, func: Callable[[A, T], A], initial: A) -> A:
        acc = initial
        for x in self.source:
            acc = func(acc, x)
        return acc

    # -----------------------
    # Sinks (consumidores)
    # -----------------------
    def to_list(self) -> List[T]:
        return list(self.source)

    def for_each(self, func: Callable[[T], None]) -> None:
        for x in self.source:
            func(x)

    def to_file(self, path: str, formatter: Callable[[T], str] = str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            for x in self.source:
                f.write(formatter(x) + "\n")
