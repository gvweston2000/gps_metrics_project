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

    log_step("Validating participation_id is a UUID format")
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    df = df[df['participation_id'].astype(str).str.fullmatch(uuid_pattern)]

    log_step('Filtering out-of-bound positions')
    df = df[
        df['pitch_x'].between(-52.5, 52.5) &
        df['pitch_y'].between(-34, 34)
    ]

    log_step("Filtering unrealistic speeds")
    df = df[df['speed'] <= 12]

    log_step("Smoothing speeds")
    df['speed_smoothed'] =  df.groupby('participation_id')['speed'].transform(
        lambda s: s.rolling(window=3, center=True).mean()
    )

    log_step("Dropping rows with NaN or negative speeds")
    df = df[df['speed'].notna() & (df['speed'] >= 0)]

    log_step("Saving cleaned dataset")
    df.to_csv("cleaned_dataset.csv", index=False)

    log_step("Calculating per-row distance")
    df['distance'] = df['speed_smoothed'].fillna(df['speed']) * 0.1

    log_step("Grouping total distance per athlete")
    total_distance = df.groupby('participation_id')['distance'].sum().reset_index()
    total_distance.columns = ['participation_id', 'total_distance_m']

    log_step("Calculating distance in speed zone 5")
    zone5_mask = df['speed_smoothed'].fillna(df['speed']).between(5.5, 6.97)
    zone5_distance = df[zone5_mask].groupby('participation_id')['distance'].sum().reset_index()
    zone5_distance.columns = ['participation_id', 'zone5_distance_m']

    log_step("Calculating top speed per athlete")
    top_speed = df.groupby('participation_id')['speed_smoothed'].max().reset_index()
    top_speed.columns = ['participation_id', 'top_speed_mps']

    log_step("Combining leaderboard metrics")
    leaderboard = total_distance.merge(zone5_distance, on='participation_id', how='left')
    leaderboard = leaderboard.merge(top_speed, on='participation_id', how='left')
    leaderboard.to_csv("leaderboard_metrics.csv", index=False)

    log_step("Create team heatmap")
    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(figsize=(10,6))
    sns.kdeplot(
        x=df['pitch_x'], y=df['pitch_y'],
        fill=True, cmap="mako", thresh=0, bw_adjust=1.5
    )

    plt.title("Team Heatmap (Time Spent On Pitch)")
    plt.xlabel("Pitch X")
    plt.ylabel("Pitch Y")
    plt.xlim(-52.5, 52.5)
    plt.ylim(-34, 34)
    plt.savefig("team-heatmap.png")
    plt.close()

if __name__ == "__main__":
    main()
