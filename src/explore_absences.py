import matplotlib.pyplot as plt
import seaborn as sns
from load_data import load_student_data

if __name__ == "__main__":
    df = load_student_data()
    print(df["absences"].describe())
    print("Students with 0 absences:", (df["absences"] == 0).sum())

    non_zero = df[df["G3"] != 0]
    print("Correlation absences vs G3 (all):", df["absences"].corr(df["G3"]))
    print("Correlation absences vs G3 (no zeros):", non_zero["absences"].corr(non_zero["G3"]))

    zero_group = df[df["G3"] == 0]
    print("Absences of the students with G3 = 0:")
    print(zero_group["absences"].describe())

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    sns.scatterplot(data=df, x="absences", y="G3", alpha=0.5, ax=axes[0])
    axes[0].set_title("All students")

    sns.scatterplot(data=non_zero, x="absences", y="G3", alpha=0.5, ax=axes[1])
    axes[1].set_title("Students with G3 not 0")

    plt.show()