from pathlib import Path

import pytest

from summarize import load_rows, summarize


DATA = Path(__file__).resolve().parents[1] / "data"


def test_load_sales():
    rows = load_rows(DATA / "sales.csv")
    assert len(rows) == 4
    assert rows[0] == {"region": "East", "amount": "100"}


def test_totals_by_region():
    totals, _ = summarize(load_rows(DATA / "sales.csv"))
    assert totals == {"East": 150.0, "West": 250.0, "North": 75.0}


def test_average_is_mean_of_regional_totals():
    _, average = summarize(load_rows(DATA / "sales.csv"))
    assert average == pytest.approx(475 / 3)


def test_average_without_rows_is_zero():
    assert summarize([]) == ({}, 0.0)
