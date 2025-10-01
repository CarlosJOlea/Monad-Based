from typing import Callable, Generic, Iterable, Iterator, List, TypeVar, Generator

T = TypeVar("T")
U = TypeVar("U")
A = TypeVar("A")


class Stream(Generic[T]):
    """
    Stream síncrono y funcional.

    Permite componer pipelines de datos de manera lazy (perezosa),
    usando transformaciones como `map`, `filter`, `flat_map`, así como
    operaciones con efectos (`tap`) y acumuladores (`scan`, `reduce`).

    Ejemplo:
        Stream.from_iterable([1, 2, 3]) \
              .map(lambda x: x * 2) \
              .filter(lambda x: x > 2) \
              .to_list()
        # => [4, 6]
    """

    def __init__(self, source: Iterable[T]):
        self.source = source

    # -----------------------
    # Fuentes (sources)
    # -----------------------
    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> "Stream[T]":
        """Crea un Stream a partir de cualquier iterable (lista, set, tuple, etc.)."""
        return cls(iterable)

    # -----------------------
    # Transformaciones
    # -----------------------
    def map(self, func: Callable[[T], U]) -> "Stream[U]":
        """Transforma cada elemento con la función dada."""
        return Stream(func(x) for x in self.source)

    def filter(self, predicate: Callable[[T], bool]) -> "Stream[T]":
        """Filtra los elementos que cumplan el predicado."""
        return Stream(x for x in self.source if predicate(x))

    def flat_map(self, func: Callable[[T], Iterable[U]]) -> "Stream[U]":
        """Mapea cada elemento a un iterable y aplana el resultado."""
        return Stream(y for x in self.source for y in func(x))

    # -----------------------
    # Side-effects
    # -----------------------
    def tap(self, func: Callable[[T], None]) -> "Stream[T]":
        """Aplica una función de efecto colateral a cada elemento sin alterar el flujo."""
        def generator() -> Generator[T, None, None]:
            for x in self.source:
                func(x)  # logging / métricas / prints
                yield x
        return Stream(generator())

    # -----------------------
    # Acumuladores
    # -----------------------
    def scan(self, func: Callable[[A, T], A], initial: A) -> "Stream[A]":
        """
        Similar a reduce, pero emite el acumulador en cada paso.
        Útil para obtener históricos de acumulación.
        """
        def generator() -> Generator[A, None, None]:
            acc = initial
            for x in self.source:
                acc = func(acc, x)
                yield acc
        return Stream(generator())

    def reduce(self, func: Callable[[A, T], A], initial: A) -> A:
        """Acumula todos los valores en un único resultado."""
        acc = initial
        for x in self.source:
            acc = func(acc, x)
        return acc

    # -----------------------
    # Sinks (consumidores)
    # -----------------------
    def to_list(self) -> List[T]:
        """Convierte el Stream a lista (forzando la evaluación)."""
        return list(self.source)
