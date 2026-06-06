import pandas as pd
from pathlib import Path

files = {
    "Distance": "data/Distance.csv",
    "HeartRate": "data/HeartRate.csv",
    "Pace": "data/Pace.csv",
}

for name, path in files.items():
    if not Path(path).exists():
        print(f"[{name}] File not found: {path}\n")
        continue

    df = pd.read_csv(path)

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
