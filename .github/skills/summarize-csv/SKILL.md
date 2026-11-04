---
name: summarize-csv
description: Run and explain the Part 1 sales-by-region report in ws-part1-github-copilot/labs/starter. Use when asked to summarize a sales CSV, check regional totals or the average, or verify the report with tests.
---

# Summarize a sales CSV

Work only in `ws-part1-github-copilot/labs/starter`. Do not read presenter answers, edit Part 2 or inspect credentials.

## Steps

1. Read `ws-part1-github-copilot/labs/starter/README.md` and use its "Business rules" section as the source of truth.
2. From the `starter` folder, run the report with the interpreter you use for tests (locally, the `.venv` in `starter`; in cloud setup, the environment's own interpreter):
   `python summarize.py data/sales.csv`
3. Run the tests from the same folder: `python -m pytest -q`.
4. Report the output, then explain the average (below).

## Explain the average

- The average is the mean of the **regional totals**, not the mean of individual sales.
- Formula: sum of all regional totals divided by the number of regions.
- Example for `data/sales.csv`: East 150, West 250, North 75 gives 475 / 3 = 158.33. Dividing by the 4 sales instead gives 118.75, which is wrong.
- With no regions (header-only CSV) the average is `0.00`.
- If the printed average does not match the rules, say so and show the calculation. Report the cause rather than silently changing code.

## Boundaries

- Do not silently fix unrelated code. Report other problems you notice and ask before changing them.
- Add or update a pytest test for any behavior change you are asked to make.
