# Stats Table Generator (CLI)

This is a small Python CLI tool I made for generating **statistics tables** from numerical data. It’s mainly meant for learning, practice, and convenience — especially when working with basic statistics in class or personal projects.

You can either load a dataset from a CSV file or enter the data manually, and the program will generate:

* a raw data table (with frequency)
* a summary table (mean, variance, standard deviation, etc.)

Both **Population** and **Sample** statistics are supported.

---

## Features 

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
* Allows switching between **Population** and **Sample** calculations
* Adjust **decimal precision**
* Saves results as CSV files
* CLI is color-coded with **arrow-key navigation**

The CLI uses colors and arrow‑key navigation to make it less painful to use.

---

## Project structure

```text
stats-table-generator/
│
├── data/            # place input CSV files here
├── saved/           # generated output files
├── README.md
├── requirements.txt # Python dependencies
├── stats_table.py   # main CLI program
```

---

## Requirements

* Python 3.8 or newer
* Install dependencies using the included `requirements.txt`.

```bash
pip install -r requirements.txt
```
The main libraries used are:

* `pandas`
* `colorama`
* `inquirer`

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

## Notes on Calculations

* **Population variance**:  

$$
\sigma^2 = \frac{\sum (x - \mu)^2}{n}
$$

* **Sample variance**:  

$$
s^2 = \frac{\sum (x - \bar{x})^2}{n - 1}
$$

Standard deviation is the square root of the variance.  
Tables use Unicode symbols (μ, σ, x̄, Σ) for readability.


---

## Limitations

* No handling for missing values (NaN)
* Large datasets may not look great in the terminal or display perfectly
* Unicode alignment may vary depending on your terminal/font

---

## Why I made this

This project started as a way to practice statistics and Python at the same time. It’s not meant to replace serious stats libraries — it’s just a simple, transparent tool that shows how the calculations work.

---

## Author

Ros N.

---

If you’re learning statistics or Python, feel free to use or modify the code.
