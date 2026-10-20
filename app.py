import streamlit as st
from src.load_data import load_student_data
import matplotlib.pyplot as plt
import numpy as np
st.set_page_config(page_title="Student Performance Analytics", layout="wide")

st.title("Student Performance Analytics")
st.write("Explore real student performance data, and soon plan your own academic progress.")
df = load_student_data()

hide_zeros = st.checkbox("Hide students with a final grade of 0")
if hide_zeros:
    df = df[df["G3"] != 0]

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


















