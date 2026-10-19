import matplotlib.pyplot as plt
from load_data import load_student_data
import numpy as np
if __name__ == "__main__":
    df = load_student_data()
    g3 = df["G3"]

    print("Mean:", g3.mean())
    print("Median:", g3.median())
    print("Min:", g3.min())
    print("Max:", g3.max())
    print("Standard deviation:", g3.std())
    print("Students with G3 = 0:", (g3 == 0).sum())
    zero_group = df[df["G3"] == 0]
    print(zero_group[["G1", "G2", "G3"]].describe())
    print("Zero-G3 students who also have G2 = 0:", (zero_group["G2"] == 0).sum())

    # plt.figure(figsize=(8, 5))
    # plt.hist(g3, bins=np.arange(-0.5, 21.5, 1), edgecolor="black")
    # print(g3.value_counts().sort_index())
    # plt.xticks(range(0, 21))
    # plt.title("Distribution of Final Mathematics Grades")
    # plt.xlabel("Final Grade (G3)")
    # plt.ylabel("Number of Students")
    # plt.show()

    g2_zero = df[df["G2"] == 0]
    print("Students with G2 = 0:", len(g2_zero))
    print("Of those, G3 = 0:", (g2_zero["G3"] == 0).sum())

    print(df[["G1", "G2", "G3"]].corr())
    non_zero = df[df["G3"] != 0]
    print(non_zero[["G1", "G2", "G3"]].corr())











