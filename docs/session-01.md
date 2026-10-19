# Session 1 Summary: Setup and Loading the Data

**Date:** 17 October 2026
**Project:** Student Performance Analytics

---

## 1. Goal

Move the project from Google Colab to VS Code, set up a clean project folder with its own virtual environment, and load the UCI student dataset using a real `.py` file.

## 2. What we built

Project folder: `student-performance-analytics`

| Item | What it is |
|---|---|
| `.venv\` | The project's private Python environment (its own copy of the libraries) |
| `data\raw\student-mat.csv` | The original maths dataset. We never edit this file. |
| `data\raw\student.txt` | Official description of every column |
| `src\load_data.py` | Our first real code file. Its only job is to load the dataset. |
| `hello.py` | A tiny test file to check that Python runs. Can be deleted later. |

Libraries installed: pandas, numpy, matplotlib, seaborn, streamlit.

## 3. Commands we used

| Command | What it does |
|---|---|
| `cd student-performance-analytics` | Moves the terminal into the project folder |
| `python --version` / `pip --version` / `git --version` | Checks that each tool is installed |
| `python -m venv .venv` | Creates the virtual environment |
| `.venv\Scripts\Activate.ps1` | Switches the environment on (the prompt shows `(.venv)`) |
| `python -m pip install ...` | Installs libraries into the active environment |
| `mkdir data\raw` | Makes a folder (`mkdir` = make directory) |
| `python src\load_data.py` | Runs our file |

## 4. Code walkthrough

### hello.py

```python
print("Hello, Tanish")
```

`print()` displays whatever is inside the brackets. The quotes mark it as text. This was only a test to prove Python and VS Code work together.

### src\load_data.py

**Segment 1: imports**

```python
from pathlib import Path
import pandas as pd
```

- `import` brings in a tool someone else wrote.
- `pandas` is the library for working with tables of data. `as pd` is its standard nickname.
- `Path` (from the built-in `pathlib`) helps us work with file locations safely.

**Segment 2: where the data lives**

```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "student-mat.csv"
```

- `__file__` is the location of this file (`.../src/load_data.py`).
- `.resolve()` turns it into a full absolute address.
- `.parent` goes up one folder. Twice takes us from the file, to `src`, to the project folder.
- With `Path` objects, `/` joins folder names. It does not divide.
- CAPITAL names are a Python convention for values that never change (constants).
- Why this way: the code finds the data no matter where we run it from.

**Segment 3: the loading function**

```python
def load_student_data():
    df = pd.read_csv(DATA_PATH, sep=";")
    return df
```

- `def` defines a function: a named, reusable set of instructions.
- `pd.read_csv` reads a CSV into a **DataFrame** (pandas' table). `df` is the usual name for it.
- `sep=";"` is needed because this file separates values with semicolons, not commas.
- `return df` hands the table back to whoever called the function.

**Segment 4: a test that only runs when this file is run directly**

```python
if __name__ == "__main__":
    df = load_student_data()
    print("Shape (rows, columns):", df.shape)
    print()
    print(df.head())
    print(df.index)
    print(df.isnull().sum().sum())
```

- `if __name__ == "__main__":` means "only do this when the file is run directly". When the Streamlit app imports `load_student_data` later, this block is skipped.
- `df.shape` gives (rows, columns). Ours: `(395, 33)`.
- `df.head()` shows the first 5 rows. Pandas hides the middle columns with `...` because they don't fit on screen, but they are still loaded.
- `df.index` shows the row labels: `RangeIndex(start=0, stop=395, step=1)`. Labels run 0 to 394, because Python counts from 0 and `stop` is not included.
- `df.isnull().sum().sum()` counts missing cells. It printed 0, so there are no missing values.

## 5. Key ideas (write these in your own words)

Fill these in yourself. A sentence or two each is enough.

- What is a virtual environment, and why does a project have its own?
- What is a DataFrame?
- What does the index on the left of a DataFrame mean? (Hint: it is not a null marker.)
- Why do we keep the original data in `data\raw` and never edit it?
- What does `python -m pip` do differently from plain `pip`?

## 6. Errors and fixes

| Error | Cause | Fix |
|---|---|---|
| `No such file or directory` when running `hello.py` and `load_data.py` | The terminal was standing in the outer folder, not the project folder | `cd student-performance-analytics`. Always read the prompt to see where the terminal is. |
| `ModuleNotFoundError: No module named 'pandas'` | Libraries were installed in a different environment from the one running the code (two `.venv` folders existed) | Activated the project's own `.venv`, installed with `python -m pip`, then deleted the extra outer `.venv` |
| Data files landed outside the project folder | Dropped onto empty space in the Explorer | Dragged them onto the `raw` folder instead |

## 7. Interview line

"I set up a Python project in VS Code with an isolated virtual environment, and wrote a loader that reads the UCI student performance dataset into a pandas DataFrame, then verified its shape and checked for missing values."

## 8. Questions I still have

(Write anything that is still fuzzy here.)

-

## 9. Not done yet

- `requirements.txt` (the saved list of libraries) has not been created yet.
- Git and GitHub are not set up yet.

## 10. Next session

Session 2: first look at the data. We will recreate the final-grade (G3) histogram in code files and interpret what it shows.

---

*Dataset: Cortez, P. and Silva, A. (2008). Student Performance. UCI Machine Learning Repository. Licensed CC BY 4.0. https://archive.ics.uci.edu/dataset/320/student%2Bperformance*
