# Session 3 Summary: Study Time, Absences and Previous Failures

**Date:** 19 October 2026
**Project:** Student Performance Analytics

---

## 1. Goal

See how three factors (study time, absences, previous failures) relate to the final maths grade (`G3`), carefully, and always checking whether the 38 students with G3 = 0 change the picture.

## 2. What we built

| File | What it does |
|---|---|
| `src\explore_factors.py` | Study time vs G3: group sizes, averages with and without the zeros, boxplots |
| `src\explore_absences.py` | Absences: summary statistics, correlation with G3, scatter plots |
| `src\explore_failures.py` | Previous failures vs G3: group sizes, averages, share of zero grades, boxplots |

## 3. What we found

### Study time (`studytime`, a category code 1 to 4, not hours)

| Category | Students | Mean G3 (all) | Mean G3 (no zeros) |
|---|---|---|---|
| 1 | 105 | 10.05 | 11.47 |
| 2 | 198 | 10.17 | 11.07 |
| 3 | 65 | 11.40 | 12.56 |
| 4 | 27 | 11.26 | 12.67 |

- Medians (boxplot, zeros removed): about 11, 11, 12, 12.5.
- It is a step between categories 2 and 3, not a steady rise. Groups 1 and 2 are about the same, and 3 and 4 are about the same.
- The groups overlap heavily: the spread inside each group is much bigger than the difference between groups.
- Group 4 is small (27 students, 24 without zeros), so its average is shaky.

### Absences (a real count)

- Mean 5.7, median 4, standard deviation 8.0, maximum 75. 115 students have 0 absences.
- The distribution is **right-skewed**: most students have few absences, and a few have many.
- **All 38 students with G3 = 0 have 0 absences.** That is unusual, and a plausible (unconfirmed) explanation is that their records are incomplete, for example students who left the course.
- Correlation of absences with G3: **0.03** with all students, **-0.21** with the zeros removed. The zero group hid a weak negative trend.
- (-0.21)² is about 0.045, so absences account for only about 4 to 5% of the differences in grades.

### Previous failures (`failures`, category 0 to 3)

| Failures | Students | Mean G3 (all) | Mean G3 (no zeros) | Share with G3 = 0 |
|---|---|---|---|---|
| 0 | 312 | 11.25 | 11.94 | 5.8% |
| 1 | 50 | 8.12 | 10.15 | 20% |
| 2 | 17 | 6.24 | 8.83 | 29% |
| 3 | 16 | 5.69 | 8.27 | 31% |

- This is the clearest pattern so far: a steady drop in grades, and a much higher chance of a final 0, as failures go up.
- But 18 of the 38 zero-grade students had no previous failures, so failures do not explain all the zeros.
- Categories 2 and 3 are small, so they should not be compared with each other. A fairer write-up merges them as "2 or more".

### Overall

All of these are **associations, not proof of cause**. Study time, absences and failures may all be influenced by other things (support at home, difficulty with the subject, and so on), and the data is a one-time snapshot of 395 students from two schools.

## 4. Code walkthrough

### Filtering and the zero group (used in every file)

```python
non_zero = df[df["G3"] != 0]
```

- `df["G3"] != 0` gives True/False for every student ("is G3 not 0?").
- `df[...]` keeps only the True rows, so `non_zero` is the 357 students with a real final grade.
- We repeat each analysis with and without the zeros because they change several results.

### explore_factors.py

**Group sizes**

```python
print(df["studytime"].value_counts().sort_index())
```

`value_counts()` counts students per category, and `.sort_index()` orders them 1, 2, 3, 4. We check this first because a small group gives an unreliable average.

**Average per group (groupby)**

```python
summary = df.groupby("studytime")["G3"].agg(["count", "mean", "median"])
```

1. `groupby("studytime")` splits the table into one small table per category.
2. `["G3"]` says we only care about G3 inside each.
3. `.agg([...])` calculates the count, mean and median for each group and joins the results into one table.

**Two boxplots side by side**

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.boxplot(data=df, x="studytime", y="G3", ax=axes[0])
axes[0].set_title("All students")
sns.boxplot(data=non_zero, x="studytime", y="G3", ax=axes[1])
axes[1].set_title("Students with G3 not 0")
plt.show()
```

- `plt.subplots(1, 2, ...)` makes one canvas with 1 row and 2 panels. `axes[0]` is the left panel and `axes[1]` is the right.
- `sns.boxplot(...)` draws one box per category, in the panel named by `ax=`.
- The panels have different vertical scales (the left starts at 0, the right at 4), so compare numbers, not heights.

**How to read a boxplot**

- Picture all students standing in a line from lowest to highest grade.
- The line inside the box is the **median** (the middle student).
- The box covers the middle half of the students (the 25% and 75% **quartiles**). A taller box means more spread.
- The whiskers stretch to the lowest and highest "normal" values.
- Dots are **outliers**, students far from the pack. A dot can hide many students stacked on the same value.

### explore_absences.py

**Summary and counting zeros**

```python
print(df["absences"].describe())
print("Students with 0 absences:", (df["absences"] == 0).sum())
```

- `describe()` gives count, mean, standard deviation, min, quartiles and max.
- The mean (5.7) is above the median (4) and the standard deviation (8.0) is larger than the mean. Together these show a right-skewed column with a few very large values.
- `(... == 0).sum()` counts the True values, which counts the students with 0 absences.

**Correlation of two columns**

```python
print(df["absences"].corr(df["G3"]))
print(non_zero["absences"].corr(non_zero["G3"]))
```

- `a.corr(b)` gives a number between -1 and +1. The sign is the direction (plus: rise together, minus: one rises while the other falls). The size is the strength.
- Rough guide: 0.9 and above is very strong, 0.5 to 0.9 clear, 0.3 to 0.5 moderate, 0.1 to 0.3 weak, under 0.1 practically none.
- Squaring the number gives roughly the share of grade differences explained by the other column.
- It only measures straight-line patterns, and it never proves cause.

**Scatter plots**

```python
sns.scatterplot(data=df, x="absences", y="G3", alpha=0.5, ax=axes[0])
```

- One dot per student: right means more absences, higher means a better grade.
- `alpha=0.5` makes dots half see-through, so darker spots show where many students overlap.
- The dark dot at the bottom-left of the left panel is the 38 zero-grade students stacked on one spot.

### explore_failures.py

**Share of zero grades per category**

```python
print((df["G3"] == 0).groupby(df["failures"]).mean())
```

- `df["G3"] == 0` gives True/False for every student.
- `.groupby(df["failures"])` splits those values by failures category, using a column from the table as the grouping key.
- `.mean()` averages the True/False values. True counts as 1 and False as 0, so the average is the **fraction of Trues**, which is the share of students with a final grade of 0.

**Optional extra: see the numbers behind each box**

```python
print(df.groupby("failures")["G3"].describe())
```

The box runs from the 25% to the 75% value, the line inside it is the 50% value (the median), and the whiskers and dots come from the min and max.

### Why the failures boxplots looked odd

- **Small groups.** Categories 2 and 3 have only 17 and 16 students (12 and 11 without zeros), so one or two students change a box a lot.
- **Boxes touching 0 (left panel).** About 30% of students in categories 2 and 3 have a final grade of 0. That is more than a quarter, so the 25% mark itself is 0 and the box starts at the floor.
- **No dot at 0 for categories 2 and 3.** A dot means "unusual for this group". A zero is unusual in category 0 (5.8%) but normal in categories 2 and 3.
- **Dots in the right panel.** The box for category 2 is very narrow because those students are bunched together. Whiskers can only stretch 1.5 times the box height past the box, so students a few points away are shown as dots.

## 5. Key ideas (write these in your own words)

- How do you read a boxplot? (median, box, whiskers, dots)
- What does a correlation of -0.21 mean, and what does it NOT mean?
- Why did the correlation between absences and G3 change from 0.03 to -0.21 when we removed the zeros?
- Why do the boxes for failures categories 2 and 3 touch 0 in the left panel but not in the right?
- Why is it risky to read much into the averages of small groups?
- Why do we say "associated with" and not "causes"?

## 6. To confirm in `student.txt`

- What are the four `studytime` categories exactly? (I believe they are under 2 hours, 2 to 5, 5 to 10 and over 10 hours per week, but this was written from memory, so check.)
- What does `failures` say about the value 3? (The data tops out at 3, so it probably means "3 or more".)

## 7. Errors and fixes

No new errors this session. (Reminder from Session 2: run files in the terminal with `(.venv)` active, not with the Code Runner play button.)

## 8. Interview lines

**Study time:** "Higher study-time categories showed slightly higher final grades, but the groups overlapped heavily, so study time alone is a weak predictor, and the data cannot show that studying causes better grades."

**Absences:** "Among students with a recorded final grade, absences had a weak negative correlation with grades (about -0.21), explaining roughly 4% of the variation. I also found that all students with a final grade of zero had zero absences, which suggests incomplete records, so I analysed them separately."

**Failures:** "Previous failures showed the clearest association: students with no failures averaged about 12 and students with three averaged about 8, and the share with a final grade of zero rose from about 6% to about 31%. The high-failure groups are small, so I treat the comparison cautiously."

## 9. Questions I still have

(Write anything that is still fuzzy here.)

-

## 10. Next session

Session 4: a correlation heatmap across the numeric columns with seaborn (being careful with category codes), then writing up the Phase 1 findings in one clear document.

---

*Dataset: Cortez, P. and Silva, A. (2008). Student Performance. UCI Machine Learning Repository. Licensed CC BY 4.0. https://archive.ics.uci.edu/dataset/320/student%2Bperformance*
