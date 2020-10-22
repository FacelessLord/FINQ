from finq import FINQ
from test.test_foreach import collector


def test_count():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = 8

    a_f = FINQ(a)

    assert a_f.count() == expected


def test_max():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = 26

    a_f = FINQ(a)

    assert a_f.max() == expected


def test_min():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = 1

    a_f = FINQ(a)

    assert a_f.min() == expected


def test_sum():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = 90

    a_f = FINQ(a)

    assert a_f.sum() == expected


def test_max_diff():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = 25

    a_f = FINQ(a)

    assert a_f.max_diff() == expected
