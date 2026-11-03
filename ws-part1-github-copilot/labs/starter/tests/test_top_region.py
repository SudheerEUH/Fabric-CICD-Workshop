from summarize import top_region


def test_top_region_normal_totals():
    totals = {"East": 150.0, "West": 250.0, "North": 75.0}
    assert top_region(totals) == ("West", 250.0)


def test_top_region_tie_returns_alphabetically_first():
    totals = {"West": 200.0, "East": 200.0, "North": 75.0}
    assert top_region(totals) == ("East", 200.0)


def test_top_region_no_totals():
    assert top_region({}) == (None, 0)
