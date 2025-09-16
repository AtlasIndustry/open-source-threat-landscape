import pandas as pd, glob, os
from pathlib import Path

KEYWORDS = ["ransomware","phishing","zero-day","APT","CVE-","SharePoint","SonicWall","LockBit","Akira"]

files = sorted(glob.glob("data/raw/rss_*.csv"))
if not files:
    raise SystemExit("No raw files in data/raw/. Run the RSS collection first.")

df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
text = (df["title"].fillna("") + " " + df["summary"].fillna("")).str.lower()

counts = {k: int(text.str.contains(k.lower(), regex=False).sum()) for k in KEYWORDS}
out = pd.DataFrame.from_dict(counts, orient="index", columns=["count"]).sort_values("count", ascending=False)

Path("data/processed").mkdir(parents=True, exist_ok=True)
out.to_csv("data/processed/keyword_counts.csv")
print("Wrote data/processed/keyword_counts.csv")
