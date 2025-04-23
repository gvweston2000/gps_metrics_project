import pandas as pd

def log_step(title):
    print(f"\n=== {title.upper()} ===")

def main():
    log_step("Loading dataset")
    df = pd.read_csv("match_data.csv")
    print(df.head(3))

    log_step("Renaming columns")
    df.rename(columns={
        'Time (s)': 'time',
        'Pitch_x': 'pitch_x',
        'Pitch_y': 'pitch_y',
        'Speed (m/s)': 'speed'
    }, inplace=True)

    log_step("Casting columns to numeric types")
    for col in ['time', 'pitch_x', 'pitch_y', 'speed']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    log_step("Basic dataset info")
    print("\n[DataFrame Info]")
    df.info()

    print("\n[Summary Statistics]")
    print(df.describe())

    print("\n[Missing Values]")
    print(df.isnull().sum())

if __name__ == "__main__":
    main()
