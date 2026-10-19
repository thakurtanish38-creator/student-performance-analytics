# Student Performance Analytics

A learning project in Python: exploring real student performance data, with a planned web app for academic planning tools.

## Status

Work in progress.

**Done:** data loading and exploratory analysis of the UCI student performance dataset (maths course).

**Planned, not built yet:** a Streamlit web app with a Target CGPA Planner, an assignment and deadline planner, an exam calculator, personal academic reports, and user accounts with a database.

## What the analysis found

Full write-up: [docs/findings.md](docs/findings.md)

- 38 of the 395 students (about 10%) have a final grade of 0, forming a separate group. All 38 also have 0 absences, which suggests incomplete records.
- Previous failures show the clearest link to the final grade: students with no failures average about 11.3, and students with three average about 5.7.
- Apart from the earlier grades (G1 and G2), no single factor has a correlation above about 0.4 with the final grade.
- These are associations in one snapshot of data, not proof of cause.

## Project structure

```
student-performance-analytics/
├── data/raw/          original dataset (never edited)
├── docs/              findings and session notes
├── src/               Python scripts
├── requirements.txt   libraries and exact versions
└── README.md
```

## How to run it (Windows PowerShell)

Developed with Python 3.14.

```
git clone <repository-url>
cd student-performance-analytics
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src\load_data.py
python src\explore_grades.py
```

Other scripts in `src`: `explore_factors.py`, `explore_absences.py`, `explore_failures.py` and `explore_correlations.py`.

## Dataset and credit

This project uses the maths file (`student-mat.csv`) from the Student Performance dataset, collected in two Portuguese secondary schools.

- Cortez, P. (2008). Student Performance [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T
- Related paper: Cortez, P. and Silva, A. (2008). Using Data Mining to Predict Secondary School Student Performance.
- Licence: Creative Commons Attribution 4.0 International (CC BY 4.0).
- Source page: https://archive.ics.uci.edu/dataset/320/student%2Bperformance

Grades in this dataset run from 0 to 20 and are secondary-school grades, not university CGPA.

## Limitations

- The findings describe one snapshot of 395 students and do not apply directly to university students.
- Many columns are category codes or ratings, so correlations are rough guides.
- Correlation does not show cause.

## Author

Built by Tanish as a first project, learning step by step.