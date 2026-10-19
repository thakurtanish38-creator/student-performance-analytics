from pathlib import Path
import pandas as pd
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "student-mat.csv"
def load_student_data():
    df = pd.read_csv(DATA_PATH, sep=";")
    return df
if __name__ == "__main__":
    df = load_student_data()
    print("Shape (rows, columns):", df.shape)
    print()
    print(df.head())
    print(df.index)
    print(df.isnull().sum().sum())