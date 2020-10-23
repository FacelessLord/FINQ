from collections import defaultdict
from random import random
from typing import Iterable, Callable, TypeVar, Generic, NoReturn, Set, List, Tuple, Dict

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")

Identity: Callable[[T], T] = lambda f: f
Consumer: NoReturn = lambda f: ()
IdentityTrue: Callable[[T], bool] = lambda f: True
IdentityFalse: Callable[[T], bool] = lambda f: False
Sum: Callable[[T, T], T] = lambda a, b: a + b
PairSum: Callable[[Tuple[T, T]], T] = lambda t: t[0] + t[1]
First: Callable[[Tuple[T]], T] = lambda t: t[0]
Second: Callable[[Tuple[T]], T] = lambda t: t[1]
Multiply: Callable[[T, T], T] = lambda a, b: a * b
Square: Callable[[T], T] = lambda a: a * a
OneArgRandom = lambda v: random()


def TupleSum(t: Tuple) -> T:
    if len(t) == 0:
        return 0
    sum = t[0]
    for i in range(1, len(t)):
        sum += t[i]
    return sum


class FINQ(Iterable[T]):
    def __init__(self, source: Iterable[T]):
        self._source = source

    def __iter__(self):
        for item in self._source:
            yield item

    def concat(self, b: Iterable[T]) -> 'FINQ[T]':
        return FINQConcat(self, b)

    def map(self, func: Callable[[T], T2]) -> 'FINQ[T2]':
        return FINQ(map(func, self))

    def zip(self, *b: List[Iterable[T2]]) -> 'FINQ[Tuple]':
        return FINQ(zip(self, *b))

    def flat_map(self, func: Callable[[T], Iterable[T2]] = Identity) -> 'FINQ[T2]':
        return FINQFlatMap(self, func)

    def filter(self, func: Callable[[T], T2]) -> 'FINQ[T2]':
        return FINQ(filter(func, self))

    def distinct(self) -> 'FINQ[T]':
        return FINQDistinct(self)

    def sort(self, func: Callable[[T], float] = Identity, /, reverse=False) -> 'FINQ[T2]':
        return FINQ(sorted(self, key=func, reverse=reverse))

    def skip(self, count: int) -> 'FINQ[T2]':
        return FINQ(o for i, o in enumerate(self, 0) if i >= count)

    def take(self, count: int) -> 'FINQ[T2]':
        return FINQ(o for i, o in enumerate(self, 0) if i < count)

    def pairs(self) -> 'FINQ[Tuple[T,T]]':
        return FINQPairs(self)

    def cartesian_product(self, b: Iterable[T1]) -> 'FINQ[Tuple[T,T1]]':
        return FINQCartesianProduct(self, b)

    def cartesian_power(self, pow: int) -> 'FINQ':
        return FINQCartesianPower(self, pow)

    def enumerate(self, start: int = 0) -> 'FINQ[Tuple[int, T]]':
        return FINQ(enumerate(self, start))

    def join(self, delimiter: str = '') -> str:
        return delimiter.join(self)

    def for_each(self, func: NoReturn = Consumer) -> NoReturn:
        for item in self:
            func(item)

    def peek(self, func: NoReturn = Identity) -> 'FINQ[T]':
        return FINQPeek(self, func)

    def group_by(self, func: Callable[[T], T2]) -> 'FINQ[List[T]]':
        return FINQGroupBy(self, func)

    def any(self, func: Callable[[T], bool] = IdentityTrue) -> bool:
        for i in self:
            if func(i):
                return True
        return False

    def none(self, func: Callable[[T], bool] = IdentityTrue) -> bool:
        for i in self:
            if func(i):
                return False
        return True

    def first(self) -> T:
        return next(iter(self))

    def random(self, percentage: float) -> 'FINQ[T]':
        return FINQ(i for i in self if random() < percentage)

    def sort_randomly(self) -> 'FINQ[T]':
        return self.sort(OneArgRandom)

    def to_list(self) -> List[T]:
        return list(self)

    def to_set(self) -> Set[T]:
        return set(self)

    def to_dict(self, key: Callable[[T], T1] = First, value: Callable[[T], T2] = Second) -> Dict[T1, T2]:
        if key == First and value == Second:
            return dict(self)
        return dict(self.map(lambda t: (key(t), value(t))))

    def count(self) -> int:
        return len(list(self))

    def min(self) -> T:
        return min(self)

    def max(self) -> T:
        return max(self)

    def sum(self) -> T:
        return sum(self) or 0

    def max_diff(self) -> T:
        max, min = None, None
        for i in self:
            if max is None or i > max:
                max = i
            if min is None or i < min:
                min = i
        return max - min

    def reduce(self, reductor: Callable[[T, T], T]) -> T:
        return next(iter(FINQReduce(self, reductor)))

    def reduce_with_first(self, first: T, reductor: Callable[[T, T], T]) -> T:
        return next(iter(FINQReduce(self, reductor, first)))


class FINQFlatMap(FINQ[T]):
    def __init__(self, source: Iterable[T], mapper: Callable[[T], T2]):
        super().__init__(source)
        self.mapper = mapper

    def __iter__(self):
        for item in self._source:
            for sub_item in self.mapper(item):
                yield sub_item


class FINQPairs(FINQ[T]):
    def __init__(self, source: Iterable[T]):
        super().__init__(source)

    def __iter__(self):
        src_list = list(self._source)
        for i in src_list:
            for item2 in src_list:
                yield i, item2


class FINQPeek(FINQ[T]):
    def __init__(self, source: Iterable[T], func: NoReturn):
        super().__init__(source)
        self.func = func

    def __iter__(self):
        for item in self._source:
            self.func(item)
            yield item


class FINQReduce(FINQ[T]):
    def __init__(self, source: Iterable[T], reductor: Callable[[T, T], T], first=None):
        super().__init__(source)
        self.reductor = reductor
        self.firstValue = first

    def __iter__(self):
        result = self.firstValue
        for item in self._source:
            if not result:
                result = item
                continue
            result = self.reductor(result, item)
        yield result


class FINQCartesianProduct(FINQ[T], Generic[T, T1]):
    def __init__(self, source: Iterable[T], b: Iterable[T1]):
        super().__init__(source)
        self.b = b

    def __iter__(self):
        b_list = list(self.b)
        for item in self._source:
            for b in b_list:
                yield item, b


class FINQCartesianPower(FINQ[T]):
    def __init__(self, source: Iterable[T], pow: int):
        super().__init__(source)
        self.pow = pow

    def __iter__(self):
        if self.pow <= 0:
            return 0
        if self.pow == 1:
            for k in self._source:
                yield k
            return
        items = list(self._source)
        for i in items:
            for j in FINQCartesianPower(items, self.pow - 1):
                if isinstance(j, tuple):
                    yield i, *j
                else:
                    yield i, j


class FINQGroupBy(FINQ[List[T]]):
    def __init__(self, source: Iterable[T], func: Callable[[T], T2]):
        super().__init__(source)
        self.func = func

    def __iter__(self):
        groups = defaultdict(list)
        for i in self._source:
            groups[self.func(i)].append(i)
        for k in groups.keys():
            yield groups[k]


class FINQDistinct(FINQ[T]):
    def __init__(self, source: Iterable[T]):
        super().__init__(source)

    def __iter__(self):
        looked = set()

        for item in self._source:
            if item not in looked:
                yield item
                looked.add(item)


class FINQConcat(FINQ[T]):
    def __init__(self, source: Iterable[T], b: Iterable[T]):
        super().__init__(source)
        self.b = b

    def __iter__(self):
        for i in self._source:
            yield i
        for i in self.b:
            yield i
