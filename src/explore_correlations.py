import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from load_data import load_student_data

NUMERIC_COLUMNS = [
    "age", "Medu", "Fedu", "traveltime", "studytime", "failures",
    "famrel", "freetime", "goout", "Dalc", "Walc", "health",
    "absences", "G1", "G2", "G3",
]

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