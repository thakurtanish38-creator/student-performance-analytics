import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
from src.load_data import load_student_data
from src.cgpa import plan_target_cgpa

st.set_page_config(page_title="Student Performance Analytics", layout="wide")

NUMERIC_COLUMNS = [
    "age", "Medu", "Fedu", "traveltime", "studytime", "failures",
    "famrel", "freetime", "goout", "Dalc", "Walc", "health",
    "absences", "G1", "G2", "G3",
]


@st.cache_data
def get_data():
    return load_student_data()


def show_overview(df):
    st.title("Student Performance Analytics")
    st.write("Explore real student performance data, and soon plan your own academic progress.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Students", len(df))
    col2.metric("Average final grade", round(df["G3"].mean(), 2))
    col3.metric("Median final grade", df["G3"].median())

    st.subheader("Distribution of final grades")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["G3"], bins=np.arange(-0.5, 21.5, 1), edgecolor="black")
    ax.set_xticks(range(0, 21))
    ax.set_xlabel("Final grade (G3)")
    ax.set_ylabel("Number of students")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("The data")
    st.dataframe(df)


def show_study_time(df):
    st.header("Study time and final grade")
    st.write("Study time is a category code from 1 to 4, not hours. Check student.txt for what each code means.")

    summary = df.groupby("studytime")["G3"].agg(["count", "mean", "median"]).round(2)
    st.dataframe(summary)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=df, x="studytime", y="G3", ax=ax)
    ax.set_xlabel("Study time category")
    ax.set_ylabel("Final grade (G3)")
    st.pyplot(fig)
    plt.close(fig)

    st.caption("This shows an association, not a cause. Groups with few students (see the count column) give unreliable averages.")


def show_absences(df):
    st.header("Absences and final grade")
    st.write("Absences is a real count: the number of classes a student missed.")

    st.dataframe(df["absences"].describe().round(2))

    correlation = df["absences"].corr(df["G3"])
    st.metric("Correlation: absences vs final grade", round(correlation, 2))

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.scatterplot(data=df, x="absences", y="G3", alpha=0.5, ax=ax)
    ax.set_xlabel("Number of absences")
    ax.set_ylabel("Final grade (G3)")
    st.pyplot(fig)
    plt.close(fig)

    st.caption("A weak link, and an association only. Tick the box in the sidebar to see how the 38 zero-grade students change the correlation.")


def show_failures(df):
    st.header("Previous failures and final grade")
    st.write("Failures is the number of past class failures, from 0 to 3. In this data, 3 probably means 3 or more. Check student.txt.")

    summary = df.groupby("failures")["G3"].agg(["count", "mean", "median"]).round(2)
    st.dataframe(summary)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=df, x="failures", y="G3", ax=ax)
    ax.set_xlabel("Previous failures")
    ax.set_ylabel("Final grade (G3)")
    st.pyplot(fig)
    plt.close(fig)

    if (df["G3"] == 0).any():
        st.subheader("Share of students with a final grade of 0, by failures")
        zero_share = ((df["G3"] == 0).groupby(df["failures"]).mean() * 100).round(1)
        st.bar_chart(zero_share, x_label="Previous failures", y_label="% of students with G3 = 0")
    else:
        st.info("Untick 'Hide students with a final grade of 0' to see the share of students in each group who ended with a 0.")

    st.caption("Groups with 2 or 3 failures are small, so compare them cautiously. This shows an association, not a cause.")


def show_correlations(df):
    st.header("Correlations between the numeric columns")
    st.write("Red means two columns rise together, blue means one rises as the other falls. Many columns are category codes or ratings, so treat the numbers as rough guides.")

    correlations = df[NUMERIC_COLUMNS].corr()
    fig, ax = plt.subplots(figsize=(11, 8))
    sns.heatmap(correlations, annot=True, fmt=".2f", cmap="coolwarm",
                vmin=-1, vmax=1, annot_kws={"size": 7}, ax=ax)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("How each column relates to the final grade")
    with_g3 = correlations["G3"].drop("G3").sort_values().round(2).rename("correlation with G3")
    st.dataframe(with_g3)

    st.caption("G1 and G2 are earlier grades in the same subject, so a strong link to G3 is expected. Correlation does not show cause.")

def show_cgpa_planner():
    st.header("Target CGPA Planner")
    st.write("Find the average GPA you need in your upcoming credits to reach a target CGPA. These are your own numbers, and they are separate from the student dataset.")

    max_gpa = st.number_input("Maximum GPA on your grading scale", min_value=1.0, value=10.0, step=0.5)

    col1, col2 = st.columns(2)
    current_cgpa = col1.number_input("Current CGPA", min_value=0.0, value=7.5, step=0.1)
    target_cgpa = col2.number_input("Target CGPA", min_value=0.0, value=8.0, step=0.1)
    completed_credits = col1.number_input("Credits completed so far", min_value=0.0, value=60.0, step=1.0)
    future_credits = col2.number_input("Credits you expect to take", min_value=0.0, value=20.0, step=1.0)

    try:
        result = plan_target_cgpa(current_cgpa, completed_credits, future_credits, target_cgpa, max_gpa)
    except ValueError as error:
        st.error(str(error))
        return

    if result["status"] == "achievable":
        st.success(result["message"])
        st.metric("Required average GPA in upcoming credits", round(result["required_gpa"], 2))
    elif result["status"] == "already_achieved":
        st.success(result["message"])
    elif result["status"] == "impossible":
        st.error(result["message"])
    else:
        st.warning(result["message"])

    st.metric("Highest CGPA you could reach", round(result["max_achievable_cgpa"], 2))

    with st.expander("How is this calculated?"):
        st.write("CGPA is credit-weighted, so a course with more credits counts for more. To reach a target, the average GPA you need over your upcoming credits is:")
        st.latex(r"\text{required GPA} = \frac{\text{target} \times (\text{completed} + \text{future}) - \text{current} \times \text{completed}}{\text{future}}")
        st.write("The highest CGPA you could reach assumes a perfect GPA in every upcoming credit.")

    st.caption("This assumes a standard credit-weighted cumulative CGPA. Universities can differ (for example, repeated courses or grade replacement), so check your own rules. This is a projection, not an official result.")
ANALYTICS_PAGES = ["Overview", "Study time", "Absences", "Failures", "Correlations"]
PLANNER_PAGES = ["Target CGPA Planner"]

st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ANALYTICS_PAGES + PLANNER_PAGES)

if page in ANALYTICS_PAGES:
    hide_zeros = st.sidebar.checkbox("Hide students with a final grade of 0")
    df = get_data()
    if hide_zeros:
        df = df[df["G3"] != 0]

if page == "Overview":
    show_overview(df)
elif page == "Study time":
    show_study_time(df)
elif page == "Absences":
    show_absences(df)
elif page == "Failures":
    show_failures(df)
elif page == "Correlations":
    show_correlations(df)
elif page == "Target CGPA Planner":
    show_cgpa_planner()