import argparse
import csv
import math


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as source:
        reader = csv.reader(source, strict=True)
        try:
            columns = next(reader)
        except StopIteration:
            raise ValueError("CSV file is empty; expected region and amount columns") from None
        except csv.Error as error:
            raise ValueError(f"line {reader.line_num}: malformed CSV: {error}") from None

        missing = {"region", "amount"} - set(columns)
        if missing:
            raise ValueError(f"missing required column(s): {', '.join(sorted(missing))}")

        region_index = columns.index("region")
        amount_index = columns.index("amount")
        rows = []
        try:
            for values in reader:
                line_number = reader.line_num
                if len(values) != len(columns):
                    raise ValueError(
                        f"line {line_number}: malformed row; expected {len(columns)} "
                        f"columns, found {len(values)}"
                    )

                region = values[region_index].strip()
                if not region:
                    raise ValueError(f"line {line_number}: region must not be blank")

                amount_text = values[amount_index]
                try:
                    amount = float(amount_text)
                except ValueError:
                    raise ValueError(
                        f"line {line_number}: invalid amount {amount_text!r}; "
                        "expected a finite nonnegative number"
                    ) from None
                if not math.isfinite(amount) or amount < 0:
                    raise ValueError(
                        f"line {line_number}: invalid amount {amount_text!r}; "
                        "expected a finite nonnegative number"
                    )
                rows.append({"region": region, "amount": amount_text})
        except csv.Error as error:
            raise ValueError(f"line {reader.line_num}: malformed CSV: {error}") from None
        return rows


def summarize(rows):
    totals = {}
    for row in rows:
        region = row["region"]
        totals[region] = totals.get(region, 0) + float(row["amount"])
    average = sum(totals.values()) / len(rows)
    return totals, average


def top_region(totals):
    raise NotImplementedError("Complete this helper in GH3.")


def main():
    parser = argparse.ArgumentParser(description="Summarize sales by region.")
    parser.add_argument("path", help="Path to the sales CSV")
    args = parser.parse_args()
    try:
        totals, average = summarize(load(args.path))
    except (OSError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")
    for region, amount in sorted(totals.items()):
        print(f"{region}: {amount:.2f}")
    print(f"Average per region: {average:.2f}")


if __name__ == "__main__":
    main()
