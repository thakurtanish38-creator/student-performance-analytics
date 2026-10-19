# Session 2 Summary: The Grade Distribution and the Zeros

**Date:** 18 October 2026
**Project:** Student Performance Analytics

---

## 1. Goal

Look at the final grades (`G3`) properly: recreate the Colab statistics in a code file, draw an honest histogram, and investigate the unusual group of students with a final grade of 0.

## 2. What we built

| Item | What it is |
|---|---|
| `src\explore_grades.py` | Our exploration script. It reuses `load_student_data()` from `load_data.py`, prints statistics, investigates the zeros, calculates correlations and draws the histogram. |

## 3. What we found

| Finding | Detail |
|---|---|
| Statistics match Colab | Median 11, min 0, max 20, standard deviation about 4.58 |
| 38 students have G3 = 0 | About 10% of the 395 students. They form a separate lump far from the rest. |
| Nobody has G3 of 1, 2 or 3 | Only one student has a 4. |
| The old histogram was misleading | With `bins=11`, most bars covered two grades at once. The "peak" at 11-12 was grades 11 and 12 added together, and the "dip" at 10 was a single grade next to double-width bars. With one bar per grade, the tallest bar is grade 10 (about 56 students). |
| The zero students did not start at zero | Their G1 minimum is 4 (mean about 7.5). Their G2 mean is about 4.7. |
| 13 of the 38 already had G2 = 0 | And all 13 students with G2 = 0 have G3 = 0. Nobody recovered from a zero in period 2. |
| Correlations (all 395 students) | G1-G2 0.85, G1-G3 0.80, G2-G3 0.90 |
| Correlations (357 students, zeros removed) | G1-G2 0.90, G1-G3 0.89, G2-G3 0.97 |

**Not yet known:** why those students have a 0. A plausible guess is that they left the course or did not sit the final assessment, but the dataset does not say, so this stays a hypothesis.

## 4. Code walkthrough

### src\explore_grades.py

**Segment 1: imports**

```python
import matplotlib.pyplot as plt
import numpy as np
from load_data import load_student_data
```

- `matplotlib.pyplot` draws charts (`plt` is its nickname).
- `numpy` is the number-crunching library underneath pandas (`np` is its nickname). We need `np.arange` for the bin edges.
- `from load_data import load_student_data` reuses our loader from Session 1. It works because both files are in `src`.

**Segment 2: load the data and pick the column**

```python
if __name__ == "__main__":
    df = load_student_data()
    g3 = df["G3"]
```

- `if __name__ == "__main__":` means "run this block only when the file is run directly".
- `df["G3"]` selects one column, called a **Series**. We store it in `g3` to avoid retyping.

**Segment 3: summary statistics**

```python
    print("Mean:", g3.mean())
    print("Median:", g3.median())
    print("Min:", g3.min())
    print("Max:", g3.max())
    print("Standard deviation:", g3.std())
    print("Students with G3 = 0:", (g3 == 0).sum())
```

- The first five lines recreate the Colab numbers.
- `g3 == 0` gives True or False for every student. `.sum()` counts the Trues, because Python treats True as 1, so this counts the zero-grade students.

**Segment 4: investigating the zeros**

```python
    zero_group = df[df["G3"] == 0]
    print(zero_group[["G1", "G2", "G3"]].describe())
    print("Zero-G3 students who also have G2 = 0:", (zero_group["G2"] == 0).sum())

    g2_zero = df[df["G2"] == 0]
    print("Students with G2 = 0:", len(g2_zero))
    print("Of those, G3 = 0:", (g2_zero["G3"] == 0).sum())
```

- `df[df["G3"] == 0]` is **filtering**: the inner part gives True/False per row, and the outer `df[...]` keeps only the True rows. `zero_group` is a smaller table of 38 students.
- `[["G1", "G2", "G3"]]` has double brackets on purpose: the inner brackets make a list of column names, and the outer ones select those columns.
- `.describe()` summarises each column (count, mean, std, min, quartiles, max).
- `len(...)` counts the rows in a table.

**Segment 5: how the grades relate (correlation)**

```python
    print(df[["G1", "G2", "G3"]].corr())

    non_zero = df[df["G3"] != 0]
    print(non_zero[["G1", "G2", "G3"]].corr())
```

- `.corr()` gives a square table of correlations between every pair of columns. Each value is between -1 and 1. Near 1 means the two move together, near 0 means no straight-line pattern, near -1 means they move in opposite directions. The diagonal is always 1.0 (a column matches itself).
- `!=` means "not equal to", so `non_zero` is the 357 students who have a real final grade.
- Removing the 38 zeros raised every correlation, because those students are outliers that break the straight-line pattern (a decent G2 followed by a final 0).

**Segment 6: the histogram**

```python
    plt.figure(figsize=(8, 5))
    plt.hist(g3, bins=np.arange(-0.5, 21.5, 1), edgecolor="black")
    plt.xticks(range(0, 21))
    plt.title("Distribution of Final Mathematics Grades")
    plt.xlabel("Final Grade (G3)")
    plt.ylabel("Number of Students")
    plt.show()
```

- `plt.figure(figsize=(8, 5))` creates the canvas.
- `plt.hist(...)` sorts values into bins and draws a bar per bin, with height showing how many students fall in it.
- `np.arange(-0.5, 21.5, 1)` makes the bin **edges** -0.5, 0.5, 1.5 ... 20.5. That gives 21 bins, each centred on one whole grade, so every grade gets its own bar.
- `plt.xticks(range(0, 21))` labels every grade from 0 to 20.
- The last lines add the title and axis labels. `plt.show()` opens the chart; close the window to let the script finish.

## 5. Key ideas (write these in your own words)

- Why did the first histogram (`bins=11`) give a misleading picture, and what fixed it?
- Why is the mean (about 10.4) lower than the median (11)?
- What do we know about the 38 students with G3 = 0, and what do we NOT know?
- What does a correlation of 0.90 mean? What does it NOT mean?
- Why did the correlations go up when we removed the zeros? Should we always remove them? Why or why not?

## 6. Errors and fixes

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'matplotlib'` | The file was run with the Code Runner play button, which uses whichever Python it finds first, not the project's `.venv` | Run it in the terminal with `(.venv)` active: `python src\explore_grades.py` |

Lesson: read the label on the error output and the prompt to see which Python actually ran.

## 7. Interview line

"I found that 10% of the students had a final grade of zero, investigated them by filtering and comparing their earlier grades, and showed that this cluster changes the correlations, so I treat it as a separate group instead of ordinary data. I also fixed a misleading histogram by choosing bins that matched the whole-number grades."

## 8. Questions I still have

(Write anything that is still fuzzy here.)

-

## 9. Next session

Session 3: study time, absences and previous failures against the final grade, using the zero group carefully. Remember: study time is a category code (1 to 4), not hours, and correlation is not causation.

---

*Dataset: Cortez, P. and Silva, A. (2008). Student Performance. UCI Machine Learning Repository. Licensed CC BY 4.0. https://archive.ics.uci.edu/dataset/320/student%2Bperformance*
