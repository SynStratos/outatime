from outatime.util.bisect import *


def test_index_of():
    _list = ['a', 'b', 'c', 'd']
    assert index_of(_list, 'b') == 1, "Wrong index returned."
    try:
        _ = index_of(_list, 'g')
        raise AssertionError("Exception not caught.")
    except ValueError:
        pass


def test_find_lt():
    _list = ['a', 'b', 'c', 'd']
    assert find_lt(_list, 'b') == 'a', "Wrong element returned."


def test_find_lte():
    _list = ['a', 'b', 'c', 'd']
    assert find_lte(_list, 'b') == 'b', "Wrong element returned."


def test_find_gt():
    _list = ['a', 'b', 'c', 'd']
    assert find_gt(_list, 'b') == 'c', "Wrong element returned."


def test_find_gte():
    _list = ['a', 'b', 'c', 'd']
    assert find_gte(_list, 'b') == 'b', "Wrong element returned."


def test_find_delimiters():
    _list = ['a', 'b', 'c', 'd']
    idx_min, idx_max = find_delimiters(_list, 'b', 'c')
    assert idx_min == 1 and idx_max == 2, "Wrong indexes returned."