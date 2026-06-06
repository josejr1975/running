import pandas as pd

# --- Load ---
distance = pd.read_csv("data/Distance.csv")
heartrate = pd.read_csv("data/HeartRate.csv")
pace = pd.read_csv("data/Pace.csv")

# --- Normalize Date columns to YYYY-MM ---

# Distance: "25-Jul" -> prepend "20" -> "2025-Jul" -> parse -> format
distance["Date"] = pd.to_datetime(
    "20" + distance["Date"], format="%Y-%b"
).dt.strftime("%Y-%m")

# HeartRate: "7/1/2025" -> parse as M/D/YYYY -> format
heartrate["Date"] = pd.to_datetime(
    heartrate["Date"], format="%m/%d/%Y"
).dt.strftime("%Y-%m")

# Pace: same M/D/YYYY format
pace["Date"] = pd.to_datetime(
    pace["Date"], format="%m/%d/%Y"
).dt.strftime("%Y-%m")

# --- Drop columns ---
distance = distance.drop(columns=["Activity"])
heartrate = heartrate.drop(columns=["Heart Rate"])
pace = pace.drop(columns=["Pace"])

# --- Summary ---
datasets = {"Distance": distance, "HeartRate": heartrate, "Pace": pace}

for name, df in datasets.items():
    print(f"{'=' * 40}")
    print(f"  {name}")
    print(f"{'=' * 40}")
    print(f"Columns : {list(df.columns)}")
    print(f"Shape   : {df.shape[0]} rows x {df.shape[1]} cols")
    print()
    print("Data types:")
    print(df.dtypes.to_string())
    print()
    print("First 5 rows:")
    print(df.head().to_string(index=False))
    print()
