import os
import pandas as pd
import anthropic
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Load ---
distance  = pd.read_csv("data/Distance.csv")
heartrate = pd.read_csv("data/HeartRate.csv")
pace      = pd.read_csv("data/Pace.csv")

# --- Normalize Date to YYYY-MM ---
distance["Date"]  = pd.to_datetime("20" + distance["Date"],  format="%Y-%b").dt.strftime("%Y-%m")
heartrate["Date"] = pd.to_datetime(heartrate["Date"], format="%m/%d/%Y").dt.strftime("%Y-%m")
pace["Date"]      = pd.to_datetime(pace["Date"],      format="%m/%d/%Y").dt.strftime("%Y-%m")

# --- Drop columns ---
distance  = distance.drop(columns=["Activity"])
heartrate = heartrate.drop(columns=["Heart Rate"])
pace      = pace.drop(columns=["Pace"])

# --- Rename Value columns ---
distance  = distance.rename(columns={"Value": "Distance"})
heartrate = heartrate.rename(columns={"Value": "HeartRate"})
pace      = pace.rename(columns={"Value": "Pace"})

# --- Merge ---
df = distance.merge(heartrate, on="Date").merge(pace, on="Date")

print(df.to_string(index=False))
print()

# --- Call Claude API ---
client = anthropic.Anthropic()

system_prompt = """You are an expert running coach who makes data-driven recommendations
to improve running practice and performance.

When analyzing data and making recommendations, always follow this structure:

1. **Notable Data Points** — What stands out in the data (highs, lows, anomalies, patterns)
2. **Performance Narrative** — What the arc of the year looks like as a whole
3. **Recommendations** — Specific, actionable things to do next based on the data

Be concrete, cite specific months and numbers from the data, and keep your tone
encouraging but honest."""

user_message = f"""Here is my monthly running data for the past 11 months.
Please analyze it and write a coaching report.

{df.to_string(index=False)}

Columns:
- Date: Month (YYYY-MM)
- Distance: Total miles run that month
- HeartRate: Average heart rate (bpm)
- Pace: Average pace (min/mile, decimal)"""

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    system=system_prompt,
    messages=[{"role": "user", "content": user_message}],
)

report = response.content[0].text

# --- Write report ---
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

report_path = output_dir / "running_report.md"
report_path.write_text(report, encoding="utf-8")

print(f"Report written to {report_path}")
print()
print(report)
