import matplotlib.pyplot as plt
import seaborn as sns
from load_data import load_student_data

if __name__ == "__main__":
    df = load_student_data()
    print("Students per failures category:")
    print(df["failures"].value_counts().sort_index())
    non_zero = df[df["G3"] != 0]

    print()
    print("G3 by failures (all students):")
    print(df.groupby("failures")["G3"].agg(["count", "mean", "median"]))

    print()
    print("G3 by failures (students with G3 != 0):")
    print(non_zero.groupby("failures")["G3"].agg(["count", "mean", "median"]))

    print()
    print("Share of students with G3 = 0, by failures category:")
    print((df["G3"] == 0).groupby(df["failures"]).mean())

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    sns.boxplot(data=df, x="failures", y="G3", ax=axes[0])
    axes[0].set_title("All students")

    sns.boxplot(data=non_zero, x="failures", y="G3", ax=axes[1])
    axes[1].set_title("Students with G3 not 0")

    plt.show()