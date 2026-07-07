import os, glob, json
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Focus-Pocus"))
CANDIDATES = [os.environ.get("FP_LOGS"),
              os.path.join(os.path.expanduser("~"), "Documents", "FocusPocus", "logs"),
              os.path.join(FP, "logs"),
              os.path.join(FP, "logs-sample")]
LOGS = next((p for p in CANDIDATES if p and os.path.isdir(p)
             and any(f.endswith(".json") for f in os.listdir(p))), None)

ALERT_INTERVAL = 10 * 60 * 1000

def clock(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).replace(tzinfo=None)

def measured_eff(focus_ms, procras):
    denom = focus_ms + procras * ALERT_INTERVAL
    return round(100 * focus_ms / denom) if denom > 0 else 0

by_day = defaultdict(list)
for fp in sorted(glob.glob(os.path.join(LOGS, "*.json"))):
    with open(fp) as fh:
        for s in json.load(fh):
            end = clock(s["timestamp"])
            start = end - timedelta(milliseconds=s["focusTime"] + s.get("pauseTime", 0))
            by_day[start.date()].append((start, end, s))

rows = []
max_sessions = 0
for d in sorted(by_day):
    sess = sorted(by_day[d], key=lambda x: x[0])
    row = {"date": d.strftime("%Y-%m-%d"), "day": d.strftime("%a")}
    total_min = 0
    for i, (start, end, s) in enumerate(sess, 1):
        total_min += s["focusTime"] / 60000
        row[f"s{i}_start"] = start.strftime("%H:%M")
        row[f"s{i}_end"] = end.strftime("%H:%M")
        row[f"s{i}_focus_min"] = round(s["focusTime"] / 60000, 1)
        row[f"s{i}_pause_min"] = round(s.get("pauseTime", 0) / 60000, 1)
        row[f"s{i}_procras"] = s["procrastinationCount"]
        row[f"s{i}_pauses"] = s["pauseCount"]
        row[f"s{i}_self_eff"] = s.get("efficiencyRating", "")
        row[f"s{i}_meas_eff"] = measured_eff(s["focusTime"], s["procrastinationCount"])
    row["n_sessions"] = len(sess)
    row["day_hours"] = round(total_min / 60, 2)
    max_sessions = max(max_sessions, len(sess))
    rows.append(row)

fields = ["start", "end", "focus_min", "pause_min", "procras", "pauses", "self_eff", "meas_eff"]
cols = ["date", "day", "n_sessions", "day_hours"]
for i in range(1, max_sessions + 1):
    cols += [f"s{i}_{f}" for f in fields]

df = pd.DataFrame(rows).reindex(columns=cols)
out_csv = os.path.join(HERE, "focus-pocus-data.csv")
df.to_csv(out_csv, index=False)
print("wrote", out_csv)
print("days:", len(df), "| max sessions/day:", max_sessions,
      "| total sessions:", int(df["n_sessions"].sum()))
print(df[["date", "day", "n_sessions", "day_hours"]].to_string(index=False))
