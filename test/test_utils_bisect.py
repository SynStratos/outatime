from outatime.util.bisect import *


def test_index_of():
    _list = [1, 2, 3, 4]

    idx = index_of(_list, 3)
    assert idx == 2, "Bad index returned."

    try:
        _ = index_of(_list, 9)
        raise AssertionError("Uncaught exception.")
    except ValueError:
        pass


def test_find_lt():
    _list = [1, 2, 3, 4]

    value = find_lt(_list, 3)
    assert value == 2, "Bad value returned."

    try:
        _ = find_lt(_list, 1)
        raise AssertionError("Uncaught exception.")
    except ValueError:
        pass


def test_find_lte():
    _list = [1, 2, 3, 4]

    value = find_lte(_list, 2)
    assert value == 2, "Bad value returned."

    try:
        _ = find_lte(_list, 0)
        raise AssertionError("Uncaught exception.")
    except ValueError:
        pass


def test_find_gt():
    _list = [1, 2, 3, 4]

    value = find_gt(_list, 3)
    assert value == 4, "Bad value returned."

    try:
        _ = find_gt(_list, 4)
        raise AssertionError("Uncaught exception.")
    except ValueError:
        pass


def test_find_gte():
    _list = [1, 2, 3, 4]

    value = find_gte(_list, 3)
    assert value == 3, "Bad value returned."

    try:
        _ = find_gte(_list, 5)
        raise AssertionError("Uncaught exception.")
    except ValueError:
        pass


def test_find_delimiters():
    _list = [1, 2, 3, 4]
    idx_min, idx_max = find_delimiters(_list, 2, 4)
    assert idx_min == 1, "Bad value returned for lower delimiter."
    assert idx_max == 3, "Bad value returned for higher delimiter."
