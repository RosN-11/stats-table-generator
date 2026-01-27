# Stats Table Generator (CLI)

This is a small Python CLI tool I made for generating **statistics tables** from numerical data. It’s mainly meant for learning, practice, and convenience — especially when working with basic statistics in class or personal projects.

You can either load a dataset from a CSV file or enter the data manually, and the program will generate:

* a raw data table (with frequency)
* a summary table (mean, variance, standard deviation, etc.)

Both **Population** and **Sample** statistics are supported.

---

## What this project does

* Lets you input numerical data (CSV or manual)
* Displays a raw data table with:

  * data values
  * deviations from the mean
  * squared deviations
  * frequencies
* Computes summary statistics:

  * Mean
  * Median
  * Mode
  * Min / Max
  * Range
  * Variance
  * Standard Deviation
* Allows switching between **Population** and **Sample** formulas
* Lets you change decimal precision
* Saves results as CSV files

The CLI uses colors and arrow‑key navigation to make it less painful to use.

---

## Project structure

```text
stats-table-generator/
│
├── stats_table.py   # main CLI program
├── data/            # place input CSV files here
├── saved/           # generated output files
├── README.md
```

---

## Requirements

* Python 3.8 or newer

Python libraries used:

```bash
pip install pandas colorama inquirer
```

---

## How to run

From the project root:

```bash
python stats_table.py
```

You’ll be prompted to:

1. Choose how to enter data (CSV or manual)
2. View the generated tables
3. Change precision or statistics type
4. Save the results if you want

Navigation is done using **arrow keys** and **Enter**.

---

## CSV input format

* CSV files must be inside the `data/` folder
* Numbers only (no headers required)
* Single or multiple columns are fine

Example:

```csv
2
4
4
6
8
```

---

## Notes on calculations

* Population variance:

  * σ² = Σ(x − μ)² / n
* Sample variance:

  * s² = Σ(x − x̄)² / (n − 1)

Standard deviation is just the square root of the variance.

Unicode symbols (μ, σ, x̄, Σ) are used in the tables mostly for readability.

---

## Limitations

* No handling for missing values (NaN)
* Large datasets may not look great in the terminal
* Unicode alignment depends on your terminal/font

---

## Why I made this

This project started as a way to practice statistics and Python at the same time. It’s not meant to replace serious stats libraries — it’s just a simple, transparent tool that shows how the calculations work.

---

## Author

Ros N.

---

If you’re learning statistics or Python, feel free to use or modify the code.
