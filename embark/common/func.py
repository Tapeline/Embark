from _typeshed import SupportsNext
from collections.abc import Callable


def first_or_none[T](iterable: SupportsNext[T]) -> T | None:
    return next(iterable, None)


def do_if_or_else[R, **P](
        condition: bool,
        true: Callable[P, R],
        false: Callable[P, R]
) -> Callable[P, R]:
    def func(*args: P.args, **kwargs: P.kwargs) -> R:
        return true(*args, **kwargs) if condition else false(*args, **kwargs)
    return func
