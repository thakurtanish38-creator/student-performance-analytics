# Phase 1 Findings: Student Performance Data

An exploratory analysis of the UCI Student Performance dataset (mathematics course). Everything below comes from Sessions 1 to 4. These are **associations in one snapshot of 395 students**, not proof of cause.

## 1. The data

- **Source:** UCI Machine Learning Repository, Student Performance dataset (mathematics file `student-mat.csv`).
- **Size:** 395 students, 33 columns.
- **Grades:** G1 (first period), G2 (second period) and G3 (final), each from 0 to 20. These are secondary-school grades, not university CGPA.
- **Data quality:** no missing values and no duplicate rows (checked in the first notebook).
- **Category codes:** many columns (study time, failures, parents' education, and ratings such as `goout`) are coded categories or 1 to 5 ratings, not true measurements.

## 2. The final grade (G3)

- Mean about 10.42, median 11, standard deviation about 4.58, range 0 to 20.
- With one bar per grade, the most common grade is **10** (about 56 students).
- **38 students (about 10%) have a final grade of 0,** forming a separate lump. No student has a grade of 1, 2 or 3, and only one has a 4.
- A histogram with too few bins made a fake peak and dip, so bins must match whole-number grades.

## 3. The students with G3 = 0

- They did **not** start at zero: their first-period grades (G1) range from 4 to 12, with a mean of about 7.5.
- Their second-period grades (G2) average about 4.7, and 13 of the 38 already had G2 = 0.
- Every student with G2 = 0 ended with G3 = 0: nobody recovered.
- **All 38 have 0 absences.**
- The reason is unknown. One possible explanation is incomplete records, such as students who left the course or did not finish, but the dataset does not say, so this is a hypothesis only.
- Because this group changes results, each analysis was repeated with and without it.

## 4. Factors compared with the final grade

| Factor | What we found |
|---|---|
| Study time (category 1 to 4) | Categories 3 and 4 average about 1 to 1.5 points higher than 1 and 2, but the groups overlap heavily. Group 4 is small (27 students). |
| Absences (a count, 0 to 75) | Most students have few; a few have many (skewed to the right). Correlation with G3: 0.03 (all) and -0.21 (zeros removed), a weak negative link explaining about 4% of the variation. |
| Previous failures (0 to 3) | The clearest pattern: average G3 falls from about 11.3 (no failures) to about 5.7 (three), and the share with G3 = 0 rises from about 6% to about 31%. Groups with 2 or more failures are small. |
| Other columns (heatmap) | All correlations with G3 are below about 0.4 apart from the earlier grades. Mother's education is weakly positive (about 0.2). Free time and family relationships are close to zero. |

Relationships among the other columns: weekday and weekend alcohol use move together (0.65), as do mother's and father's education (0.62).

## 5. Limits of this analysis

- **Association, not causation.** Study time, absences and failures may all be influenced by other things, such as support at home or difficulty with the subject.
- **Small groups** (for example 2 or 3 previous failures) give unreliable averages.
- **Category codes and ratings** make correlations rough guides.
- **Correlation only measures straight-line patterns.** A value near zero does not rule out other kinds of relationship.
- **Earlier grades (G1, G2) are not independent factors.** They measure the same subject earlier, so a strong link to G3 is expected.
- **The zero-grade group is not understood.** Results are shown with and without it.
- **Secondary-school data.** These findings do not apply directly to university students.

## 6. What this means for the app

- The analytics dashboard should let users view the data **with and without** the zero-grade students.
- Charts should use one bar per grade for the grade histogram, and avoid causal wording.
- Personal academic records stay separate from this public dataset.

---

*Dataset: Cortez, P. and Silva, A. (2008). Student Performance. UCI Machine Learning Repository. Licensed CC BY 4.0. https://archive.ics.uci.edu/dataset/320/student%2Bperformance*
