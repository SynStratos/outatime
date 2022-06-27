from outatime.util.relativedelta import relativedelta


def test_total_rounded_days():
    rd = relativedelta(years=1)

    assert rd.__total_rounded_days__ == 365, "Unexpected total days count."

    rd = relativedelta(years=1, months=1)

    assert rd.__total_rounded_days__ == 395, "Unexpected total days count."

    rd = relativedelta(years=1, months=1, days=5)

    assert rd.__total_rounded_days__ == 400, "Unexpected total days count."


def test_total_months():
    years = 2
    months = 4
    days = 200
    rd = relativedelta(years=years, months=months, days=days)

    assert rd.total_months == years*12 + months + days/30, "Unexpected total months count."


def test_total_years():
    years = 2
    months = 4
    days = 200

    rd = relativedelta(years=years, months=months, days=days)

    assert rd.total_years == years + months/12 + days/365, "Unexpected total years count."


def test_operators():
    rd = relativedelta(days=42)

    assert rd.__eq__(relativedelta(days=42)), "Bad result for == operator."
    assert rd.__ge__(relativedelta(days=42)), "Bad result for >= operator."
    assert rd.__ge__(relativedelta(days=41)), "Bad result for >= operator."
    assert rd.__le__(relativedelta(days=43)), "Bad result for <= operator."
    assert rd.__le__(relativedelta(days=42)), "Bad result for <= operator."
    assert rd.__gt__(relativedelta(days=41)), "Bad result for > operator."
    assert rd.__lt__(relativedelta(days=43)), "Bad result for < operator."
