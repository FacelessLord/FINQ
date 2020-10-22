from typing import Iterable, Callable, TypeVar, Generic, Collection, Any, NoReturn, Set, List

T = TypeVar("T")
T2 = TypeVar("T2")


class FINQ(Iterable[T]):
    """Note this class is subject to copyright
       Authored by FacelessLord"""

    def __init__(self, source: Iterable[T]):
        self.source = source

    def __iter__(self):
        for item in self.source:
            yield item

    def map(self, func: Callable[[T], T2]) -> 'FINQ[T2]':
        return FINQ(map(func, self))

    def flat_map(self, func: Callable[[T], Collection[T2]] = lambda f: f) -> 'FINQ[T2]':
        return FINQFlatMap(self, func)

    def filter(self, func: Callable[[T], T2]) -> 'FINQ[T2]':
        return FINQ(filter(func, self))

    def sort(self, func: Callable[[T], float]) -> 'FINQ[T2]':
        return FINQ(sorted(self, key=func))

    def skip(self, count: int) -> 'FINQ[T2]':
        return FINQ(o for i, o in enumerate(self, 0) if i >= count)

    def take(self, count: int) -> 'FINQ[T2]':
        return FINQ(o for i, o in enumerate(self, 0) if i < count)

    def pairs(self) -> 'FINQ[T2]':
        return FINQPairs(self)

    def enumerate(self, start: int = 0) -> 'FINQ[T2]':
        return FINQ(enumerate(self, start))

    def join(self, delimiter: str) -> str:
        return delimiter.join(self)

    def for_each(self, func: NoReturn = lambda f: ()) -> NoReturn:
        for item in self:
            func(item)

    def any(self, func: Callable[[T], bool] = lambda f: True) -> bool:
        for i in self:
            if func(i):
                return True
        return False

    def none(self, func: Callable[[T], bool] = lambda f: True) -> bool:
        for i in self:
            if func(i):
                return False
        return True

    def peek(self, func: NoReturn = lambda f: f) -> 'FINQ[T2]':
        return FINQPeek(self, func)

    def first(self) -> T:
        return next(iter(self))

    def to_list(self) -> List[T]:
        return list(self)

    def to_set(self) -> Set[T]:
        return set(self)

    def count(self) -> int:
        return len(list(self))

    def min(self) -> T:
        return min(self)

    def max(self) -> T:
        return max(self)

    def sum(self) -> T:
        return sum(self)

    def max_diff(self) -> T:
        # todo double enumeration
        return max(self) - min(self)

    def reduce(self, reductor: Callable[[T,T], T]) -> T:
        return FINQReduce(self, reductor)

    def reduce_with_first(self, first: T, reductor: Callable[[T,T], T]) -> T:
        return FINQReduce(self, reductor, first)


class FINQFlatMap(FINQ[T]):
    def __init__(self, source: Iterable[T], mapper: Callable[[T], T2]):
        super().__init__(source)
        self.mapper = mapper

    def __iter__(self):
        for item in self.source:
            for sub_item in map(self.mapper, item):
                yield sub_item


class FINQPairs(FINQ[T]):
    def __init__(self, source: Iterable[T]):
        super().__init__(source)

    def __iter__(self):
        src_list = list()
        for i in self.source:
            src_list.append(i)
            for item2 in src_list:
                yield i, item2


class FINQPeek(FINQ[T]):
    def __init__(self, source: Iterable[T], func: NoReturn):
        super().__init__(source)
        self.func = func

    def __iter__(self):
        for item in self.source:
            self.func(item)
            yield item


class FINQReduce(FINQ[T]):
    def __init__(self, source: Iterable[T], reductor: Callable[[T,T], T], first=None):
        super().__init__(source)
        self.reductor = reductor
        self.firstValue = first

    def __iter__(self):
        result = self.firstValue
        for item in self.source:
            if not result:
                result = item
                continue
            result = self.reductor(result, item)
        yield result
