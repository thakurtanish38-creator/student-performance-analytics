import matplotlib.pyplot as plt
import seaborn as sns
from load_data import load_student_data

if __name__ == "__main__":
    df = load_student_data()
    print("Students per study-time category:")
    print(df["studytime"].value_counts().sort_index())

    summary = df.groupby("studytime")["G3"].agg(["count", "mean", "median"])
    print()
    print("G3 by study time (all students):")
    print(summary)

    non_zero = df[df["G3"] != 0]
    summary_no_zero = non_zero.groupby("studytime")["G3"].agg(["count", "mean", "median"])

    print()
    print("G3 by study time (students with G3 != 0):")
    print(summary_no_zero)

    # fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    # sns.boxplot(data=df, x="studytime", y="G3", ax=axes[0])
    # axes[0].set_title("All students")
    # sns.boxplot(data=non_zero, x="studytime", y="G3", ax=axes[1])
    # axes[1].set_title("Students with G3 not 0")
    # plt.show()

    