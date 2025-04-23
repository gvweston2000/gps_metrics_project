# GPS Metrics Analysis (Player Tracking Leaderboard)

This project analyses player tracking data collected via GPS sensors during a match. It calculates key performance metrics, cleans noisy data, and visualises spatial patterns using heatmaps. The goal is to provide meaningful, coach-friendly insights such as:

- Total distance covered.  

- Distance in high-intensity sprinting (Speed Zone 5).

- Top speed per athlete.

- Pitch heatmap for positional trends.

## Project Setup

### Requirements

- Python 3.9+  

- Virtual environment recommended.

### Installation

Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```
pip install pandas matplotlib seaborn
```

## Results

- Load and explore the dataset.

- Clean and filter based on pitch bounds and speed.

- Smooth GPS speed data.

- Calculate metrics: total distance, zone 5 effort, top speed.

- Save visual insights as .png files.

- Output a leaderboard CSV for easy review.