from pathlib import Path

import pytest

from summarize import load, main, summarize


DATA = Path(__file__).resolve().parents[1] / "data"


def test_load_sales():
    rows = load(DATA / "sales.csv")
    assert len(rows) == 4
    assert rows[0] == {"region": "East", "amount": "100"}


def test_totals_by_region():
    totals, _ = summarize(load(DATA / "sales.csv"))
    assert totals == {"East": 150.0, "West": 250.0, "North": 75.0}


def test_load_trims_regions_and_accepts_zero(tmp_path):
    path = tmp_path / "sales.csv"
    path.write_text("region,amount\n East ,0\n", encoding="utf-8")

    rows = load(path)

    assert rows == [{"region": "East", "amount": "0"}]
    assert summarize(rows)[0] == {"East": 0.0}


def test_load_rejects_missing_column():
    with pytest.raises(ValueError, match="missing required column"):
        load(DATA / "missing-column.csv")


def test_load_rejects_supplied_invalid_amount():
    with pytest.raises(ValueError, match=r"line 3: invalid amount"):
        load(DATA / "invalid-amount.csv")


@pytest.mark.parametrize("amount", ["-1", "nan", "inf", "-inf"])
def test_load_rejects_negative_and_nonfinite_amounts(tmp_path, amount):
    path = tmp_path / "sales.csv"
    path.write_text(f"region,amount\nEast,{amount}\n", encoding="utf-8")

    with pytest.raises(ValueError, match=r"line 2: invalid amount"):
        load(path)


def test_load_rejects_blank_regions(tmp_path):
    path = tmp_path / "sales.csv"
    path.write_text("region,amount\n   ,10\n", encoding="utf-8")

    with pytest.raises(ValueError, match=r"line 2: region must not be blank"):
        load(path)


def test_load_rejects_zero_byte_file(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="CSV file is empty"):
        load(path)


@pytest.mark.parametrize("row", ["East,10,extra", "East", 'East,"10'])
def test_load_rejects_malformed_rows_with_line_number(tmp_path, row):
    path = tmp_path / "sales.csv"
    path.write_text(f"region,amount\n{row}\n", encoding="utf-8")

    with pytest.raises(ValueError, match=r"line 2:"):
        load(path)


def test_invalid_input_does_not_print_partial_report(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["summarize.py", str(DATA / "invalid-amount.csv")])

    with pytest.raises(SystemExit) as error:
        main()

    captured = capsys.readouterr()
    assert error.value.code != 0
    assert captured.out == ""
    assert "line 3" in captured.err
    assert "Traceback" not in captured.err
