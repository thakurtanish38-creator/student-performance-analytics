# Session 4 Summary: The Correlation Heatmap

**Date:** 19 October 2026
**Project:** Student Performance Analytics

---

## 1. Goal

See how every numeric column relates to every other one in a single picture (a correlation heatmap), find which factors relate most to the final grade `G3`, and finish the data-analysis phase.

## 2. What we built

| File | What it does |
|---|---|
| `src\explore_correlations.py` | Calculates correlations for 16 numeric columns, prints how each relates to G3, and draws two heatmaps (all students, and the 357 students with G3 not 0) |

## 3. What we found

### Correlation of each column with G3 (sorted by the zeros-removed column)

| Column | All students | Zeros removed |
|---|---|---|
| failures | -0.36 | -0.29 |
| absences | 0.03 | -0.21 |
| Walc (weekend alcohol) | -0.05 | -0.19 |
| goout | -0.13 | -0.18 |
| Dalc (weekday alcohol) | -0.05 | -0.14 |
| age | -0.16 | -0.14 |
| traveltime | -0.12 | -0.10 |
| health | -0.06 | -0.08 |
| freetime | 0.01 | -0.02 |
| famrel | 0.05 | 0.04 |
| studytime | 0.10 | 0.13 |
| Fedu (father's education) | 0.15 | 0.16 |
| Medu (mother's education) | 0.22 | 0.19 |
| G1 | 0.80 | 0.89 |
| G2 | 0.90 | 0.97 |

### What it says

- **Failures is the strongest factor outside the grades** (-0.36 with all students). Medu is the strongest *positive* factor (0.22), but failures is bigger in size.
- **Nothing outside the grades goes beyond about 0.36.** No single factor here predicts the final grade strongly, and each one explains only a small share of why students differ.
- **Freetime and famrel are close to zero** (0.01 and 0.05), meaning no straight-line relationship with G3.
- **G1 and G2 are strongly related to G3, but this is expected.** They are earlier grades in the same subject, so they are not independent factors.
- **The zeros matter:** absences changed from 0.03 to -0.21, and Walc from -0.05 to -0.19. Failures got weaker (-0.36 to -0.29), partly because students with failures are more likely to end with a 0, so the zeros were adding to that link.

### Relationships between the other columns (not with G3)

- **Dalc and Walc: 0.65.** Students who drink on weekdays tend to drink at weekends.
- **Medu and Fedu: 0.62.** The two parents' education levels tend to match.
- **Walc and goout: 0.42.** Students who go out more tend to drink more at weekends.
- Remember that these are associations, not explanations.

## 4. Code walkthrough

### src\explore_correlations.py

**Segment 1: imports**

```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from load_data import load_student_data
```

The usual tools. `pandas` is needed this time to build a small table by hand.

**Segment 2: the columns we use**

```python
NUMERIC_COLUMNS = [
    "age", "Medu", "Fedu", "traveltime", "studytime", "failures",
    "famrel", "freetime", "goout", "Dalc", "Walc", "health",
    "absences", "G1", "G2", "G3",
]
```

- A **list** holds several items in square brackets. This one holds the 16 columns that contain numbers.
- The other 17 columns contain words, and correlation needs numbers.
- Capital letters mean a constant (a value that never changes).
- Only `age`, `absences` and the grades are true measurements. The rest are category codes or ratings, so their correlations are rough guides.

**Segment 3: a function that draws one heatmap**

```python
def draw_heatmap(data, title):
    correlations = data[NUMERIC_COLUMNS].corr()
    plt.figure(figsize=(12, 9))
    sns.heatmap(
        correlations,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        annot_kws={"size": 7},
    )
    plt.title(title)
```

- We use a function so the drawing code is written once and used for both heatmaps.
- `data[NUMERIC_COLUMNS].corr()` gives a 16 by 16 table of correlations for every pair.
- `sns.heatmap(...)` draws that table as coloured squares: `annot=True` writes the numbers, `fmt=".2f"` shows two decimals, `cmap="coolwarm"` uses blue-white-red, `vmin=-1, vmax=1` fixes the colour scale so the same colour means the same thing in both charts, and `annot_kws` makes the numbers small enough to fit.

**Segment 4: running it**

```python
if __name__ == "__main__":
    df = load_student_data()
    non_zero = df[df["G3"] != 0]

    comparison = pd.DataFrame({
        "all_students": df[NUMERIC_COLUMNS].corr()["G3"],
        "zeros_removed": non_zero[NUMERIC_COLUMNS].corr()["G3"],
    })
    comparison = comparison.drop("G3").sort_values("zeros_removed")
    print(comparison.round(2))

    draw_heatmap(df, "Correlations: all students")
    draw_heatmap(non_zero, "Correlations: students with G3 not 0")
    plt.show()
```

- `.corr()["G3"]` takes the G3 column of the table: how every other column relates to the final grade.
- `pd.DataFrame({...})` builds a new table with the two versions side by side.
- `.drop("G3")` removes G3 against itself (always 1.0). `.sort_values(...)` sorts the rows, and `.round(2)` shows two decimals.
- Two windows open, and both must be closed for the program to finish.

### How to read a correlation heatmap

- Each square is the correlation between the column on its row and the column on its side.
- **Red** means positive (rise together), **blue** means negative (one rises as the other falls), and **pale** means near zero.
- The diagonal is always 1.0, because a column matches itself.
- The grid is a mirror image: the top-right repeats the bottom-left.
- Find a pair by following one column's row across to the other column.

## 5. Key ideas (write these in your own words)

- What does a heatmap show that comparing one pair at a time does not?
- Which column has the strongest relationship with G3 apart from G1 and G2? Is it positive or negative?
- Why are G1 and G2 not interesting "factors" for explaining G3?
- Why do we treat the correlations for columns like `Medu` or `goout` as rough guides?
- Why did failures get weaker when we removed the zeros?
- Why is "no relationship in the heatmap" not the same as "no relationship at all"? (Hint: correlation only measures straight-line patterns.)

## 6. To confirm in `student.txt`

- What do the codes for `Medu` and `Fedu` mean? (I believe 0 to 4, from none to higher education, but check.)
- What are the exact `studytime` categories, and what does it say about `failures` equal to 3? (Still open from Session 3.)

## 7. Errors and fixes

No errors this session.

## 8. Interview lines

**Heatmap:** "I used a correlation heatmap to compare all numeric columns at once, and found that apart from earlier grades, previous failures had the strongest association with the final grade (about -0.36), while factors like free time and family relationships showed almost none."

**Honest limits:** "No single non-grade factor had a correlation above about 0.4, so none predicts final grades strongly. Many columns are category codes or ratings, so the correlations are rough, and none of them show cause."

## 9. Questions I still have

(Write anything that is still fuzzy here.)

-

## 10. Next session

Session 5: Git and GitHub. We save the project with version history, create `requirements.txt` and a README with the dataset attribution, and put it online.

---

*Dataset: Cortez, P. and Silva, A. (2008). Student Performance. UCI Machine Learning Repository. Licensed CC BY 4.0. https://archive.ics.uci.edu/dataset/320/student%2Bperformance*
