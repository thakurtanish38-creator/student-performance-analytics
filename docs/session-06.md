# Session 6 Summary: Our First Streamlit Page

**Date:** 20 October 2026
**Project:** Student Performance Analytics

---

## 1. Goal

Turn a Python file into a web page that runs in the browser, with a heading, a checkbox, summary numbers, a chart and a data table.

## 2. What we built

| Item | What it is |
|---|---|
| `app.py` | The app's front door, at the top level of the project. It loads the data and draws the page. |

Run it with:

```
streamlit run app.py
```

Streamlit starts a small web server **on your own computer** and opens `http://localhost:8501`. `localhost` means "this computer", so nobody else can see the page. Stop it with **Ctrl + C** in the terminal.

## 3. The big idea: Streamlit reruns the whole file

When you click something on the page, Streamlit runs `app.py` again from the first line to the last. A widget (such as a checkbox) hands your code its new value on that fresh run. This lets you write ordinary top-to-bottom Python, and the page redraws to match.

When you save the file, a notice appears in the browser. **Always rerun** makes the page refresh on every save.

## 4. What we found

Ticking "Hide students with a final grade of 0":

| Number | All students | Zeros hidden |
|---|---|---|
| Students | 395 | 357 |
| Average final grade | 10.42 | 11.52 |
| Median final grade | 11.0 | 11.0 |

- The count drops by exactly 38, the zero-grade group from Session 2.
- The **average** rises, because those 38 zeros drag it down.
- The **median** stays at 11.0, because the middle student lands inside the big block of students who scored 11 either way.
- The median is **robust** (a few extreme values barely move it) and the mean is **sensitive** (extreme values pull it). This is why it is good to show both.
- On the chart, the bar at grade 0 disappears and the other bars stay the same.

## 5. Code walkthrough

### app.py

**Segment 1: imports**

```python
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from src.load_data import load_student_data
```

- `streamlit as st` brings in Streamlit (`st` is the nickname).
- `from src.load_data import ...` reuses our loader. `src.load_data` means "the file `load_data.py` inside the folder `src`". It needs the folder name because `app.py` sits one level above `src`, while the scripts inside `src` can import each other directly.
- matplotlib and numpy are the same tools we used for the histogram in Session 2.

**Segment 2: page setup and heading**

```python
st.set_page_config(page_title="Student Performance Analytics", layout="wide")

st.title("Student Performance Analytics")
st.write("Explore real student performance data, and soon plan your own academic progress.")
```

- `st.set_page_config(...)` sets the browser tab title and uses the full page width. It must be the first Streamlit command in the file.
- `st.title(...)` draws a big heading.
- `st.write(...)` is the all-purpose "show this" command: it shows text, tables or charts.

**Segment 3: load the data and add a checkbox**

```python
df = load_student_data()

hide_zeros = st.checkbox("Hide students with a final grade of 0")
if hide_zeros:
    df = df[df["G3"] != 0]
```

- `st.checkbox("...")` draws a tick box and **returns** `True` when ticked and `False` when not.
- `if hide_zeros:` runs the next line only when the box is ticked.
- `df[df["G3"] != 0]` is the same filter as in Session 2: it keeps the 357 students with a real final grade.

**Segment 4: summary numbers**

```python
col1, col2, col3 = st.columns(3)
col1.metric("Students", len(df))
col2.metric("Average final grade", round(df["G3"].mean(), 2))
col3.metric("Median final grade", df["G3"].median())
```

- `st.columns(3)` splits the page into three side-by-side columns.
- `.metric("label", value)` shows a big number with a label.
- `len(df)` counts rows, `.mean()` and `.median()` are the Session 2 statistics, and `round(..., 2)` keeps two decimals.

**Segment 5: the histogram**

```python
st.subheader("Distribution of final grades")
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(df["G3"], bins=np.arange(-0.5, 21.5, 1), edgecolor="black")
ax.set_xticks(range(0, 21))
ax.set_xlabel("Final grade (G3)")
ax.set_ylabel("Number of students")
st.pyplot(fig)
plt.close(fig)
```

- `plt.subplots(...)` returns two things: `fig` (the whole canvas) and `ax` (the drawing area). Inside Streamlit we call methods on `ax` instead of `plt.` directly.
- `ax.hist(...)` draws one bar per grade, using the bin edges from Session 2.
- `st.pyplot(fig)` shows the chart on the page. We do not use `plt.show()`, which would open a separate window.
- `plt.close(fig)` frees the canvas. The script reruns on every click, so without it unused charts would pile up in memory.

**Segment 6: the table**

```python
st.subheader("The data")
st.dataframe(df)
```

`st.subheader` draws a smaller heading, and `st.dataframe(df)` shows the table. You can scroll it and click a column heading to sort.

## 6. Key ideas (write these in your own words)

- What does "Streamlit reruns the whole file" mean, and what does a widget hand back to your code?
- Why did the average change when the zeros were hidden, but not the median?
- What is the difference between a **robust** and a **sensitive** statistic?
- Why do we use `st.pyplot(fig)` and not `plt.show()`?
- What does `localhost` mean, and who can see your page?

## 7. Errors and fixes

| Problem | Cause | Fix |
|---|---|---|
| Streamlit asked for an email and rejected `thakur` | A first-run welcome prompt for newsletters. It is optional. | Leave the field empty and press Enter |

## 8. Interview lines

**Streamlit:** "I built a Streamlit page that loads the dataset, shows summary statistics and a histogram, and lets the user hide the zero-grade group to see how it changes the mean but not the median. Streamlit reruns the script on every interaction, so widgets just return values to ordinary Python."

**Mean vs median:** "The mean rose from 10.4 to 11.5 when I hid 38 zero grades, while the median stayed at 11, which shows the median is robust to extreme values."

## 9. Questions I still have

(Write anything that is still fuzzy here.)

-

## 10. Next session

Session 7: grow the page into a dashboard. A sidebar to move between sections, charts for study time, absences and failures, the correlation heatmap, and `st.cache_data` so the data is not reloaded on every click.

---

*Dataset: Cortez, P. (2008). Student Performance [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T. Licensed CC BY 4.0.*
