from outatime.timeseries.filter_parser import FilterParserError
from test.utils import data_generation


def test_time_series_query():
    tsl = data_generation()

    query = "month > 10"
    filtered_tsl = tsl.query(query)
    assert id(tsl) != id(filtered_tsl), "Objects' identities are the same."


def test_time_series_query_inplace():
    tsl = data_generation()

    query = "month > 10"
    tsl.query(query, inplace=True)
    for element in tsl:
        assert element.day.month > 10, "Unexpected day after query."


def test_time_series_simple_queries():
    tsl = data_generation()

    query = "month > 10"
    filtered_tsl = tsl.query(query)
    assert id(tsl) != id(filtered_tsl), "Objects' identities are the same."

    for element in filtered_tsl:
        assert element.day.month > 10, "Unexpected day after query."

    query = "month == 10"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 10, "Unexpected day after query."

    query = "day < 2"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.day < 2, "Unexpected day after query."

    query = "year > 2021"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.year > 2021, "Unexpected day after query."


def test_time_series_range_queries():
    tsl = data_generation()

    query = "8 < month < 10"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert 8 < element.day.month < 10, "Unexpected day after query."

    query = "8 >= month >= 10"
    filtered_tsl = tsl.query(query)
    assert len(filtered_tsl) == 0, "Unexpected day after query."


def test_time_series_binary_queries():
    tsl = data_generation()

    query = "(month == 5) and (day == 1)"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 5 and element.day.day == 1, "Unexpected day after query."

    query = "(month == 5) or (day == 1)"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 5 or element.day.day == 1, "Unexpected day after query."

    query = "((month == 5) and (day == 1)) and year == 2021"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 5 and element.day.day == 1 and element.day.year == 2021, "Unexpected day after query."


def test_time_series_calc_queries():
    tsl = data_generation()

    query = "month == 4+4"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 8, "Unexpected day after query."

    query = "month == 2*4"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 8, "Unexpected day after query."

    query = "month == 10-2"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 8, "Unexpected day after query."

    query = "month == 2 - (-6)"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 8, "Unexpected day after query."

    query = "month == 2 - (-12+6)"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 8, "Unexpected day after query."

    query = "month == 2 - (-2*3)"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 8, "Unexpected day after query."

    query = "month == 17 % 2"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 1, "Unexpected day after query."

    query = "month == 17 // 2"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 8, "Unexpected day after query."

    query = "month == 3 ** 3"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 9, "Unexpected day after query."

    query = "month == |-9|"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 9, "Unexpected day after query."

    query = "month == |-3*3|"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 9, "Unexpected day after query."

    query = "month == |-12+3|"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 9, "Unexpected day after query."

    query = "month == |(-12+3)|"
    filtered_tsl = tsl.query(query)
    for element in filtered_tsl:
        assert element.day.month == 9, "Unexpected day after query."


def test_time_series_bad_request():
    tsl = data_generation()

    query = "month == bad_req"
    try:
        _ = tsl.query(query)
        raise AssertionError("Uncaught exception.")
    except FilterParserError:
        pass

    query = "bad_req"
    try:
        _ = tsl.query(query)
        raise AssertionError("Uncaught exception.")
    except FilterParserError:
        pass
