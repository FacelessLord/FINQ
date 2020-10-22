# FINQ
Lightweight conveyor data processing python framework, which allows to quickly write long queries without a fear that it'll become unreadable, 
because FINQ as opposed to standard library allows you to write each logical part of query at next line without tearing it and expanding logical block over whole function


# Basic functions
| Function                                         | IsTerminal | Description                                                                                                               |
|--------------------------------------------------|------------|---------------------------------------------------------------------------------------------------------------------------|
| `map(f:T1 -> T2)`                                | -          | Applies given function to every element of sequence.                                                                      |
| `flat_map(f:T1 -> TCollection = λ t -> t)`       | -          | Applies given function to every element to get collection, then glues these collections.                                  |
| `filter(f:T -> bool)`                            | -          | Removes elements that doesn't satisfy predicate from sequence.                                                            |
| `sort(f:T -> int)`                               | -          | Sorts sequence elements by key given by _f_.                                                                              |
| `skip(count:int)`                                | -          | Skips _count_ elements from sequence.                                                                                     |
| `take(count:int)`                                | -          | Limits sequence by _count_ elements, dropping other.                                                                      |
| `pairs()`                                        | -          | Returns Cartesian square of sequence.                                                                                     |
| `enumerate(start=0)`                             | -          | Maps sequence elements to pair which first value is index in sequence starting by _start_.                                |
| `join(delimiter:str)`                            | +          | Joins sequence by _delimiter_.                                                                                            |
| `for_each(f:T -> ())`                            | +          | Calls _f_ for every element of a sequence. Equivalent to:<br> <code>for e in collection:</code><br><code>    f(e)</code>. |
| `any(f:T -> bool = λ t -> True)`                 | +          | Checks if there exist element in sequence that satisfies predicate.                                                       |
| `max()`                                          | +          | Finds maximal element in sequence.                                                                                        |
| `sum()`                                          | +          | Sums all elements of sequence. Works only for summable types.                                                             |
| `max_diff()`                                     | +          | Counts maximal difference between elements. Equal to difference between max and min for sequence.                         |
| `reduce(f:T -> T)`                               | +          | Applies function to first two elements, then to result and next element until elements end.                               |
| `none(f:T -> bool = λ t -> True`                 | +          | Checks if there no element in sequence that satisfies predicate.                                                          |
| `peek(f:T -> ())`                                | -          | Applies function to each element in sequence leaving sequence unchanged.                                                  |
| `first()`                                        | +          | Takes first element of sequence.                                                                                          |
| `to_list()`                                      | +          | Creates default python-list containing all sequence elements.                                                             |
| `to_set()`                                       | +          | Creates default python-set containing all distinct sequence elements.                                                     |
| `count()`                                        | +          | Returns count of elements in sequence.                                                                                    |
| `min()`                                          | +          | Finds minimal element in sequence.                                                                                        |
| `reduce_with_first`                              | +          | Applies function to first two elements, then to result and next element until elements end. Allows to specify first element. |
