from outatime.timeseries.expr import union, intersection

from test.utils import data_generation, compare


def take_first_available(a, b):
    if a is not None:
        return a
    elif b is not None:
        return b
    else:
        raise Exception("Both arguments are None.")


def test_union():
    ts_sx = data_generation()[:10]
    ts_dx = data_generation()[5:15]

    res = union(ts_sx, ts_dx, conflict_method=take_first_available)
    expected_res = list(ts_sx) + list(ts_dx[10:])
    assert len(res) == 15, "Unexpected length of union result."
    assert compare(expected_res, res), "Unexpected union result."


def test_intersection():
    ts_sx = data_generation(empty_data=None)[:10]
    ts_dx = data_generation(empty_data_step=3)[5:15]

    res = intersection(ts_sx, ts_dx, conflict_method=take_first_available)
    expected_res = [ts_dx[0], ts_sx[6], ts_dx[2], ts_sx[8], ts_dx[4]]
    assert len(res) == 5, "Unexpected length of intersection result."
    assert compare(expected_res, res), "Unexpected intersection result."
