import re, glob, pandas as pd
from pathlib import Path
from datetime import datetime

KEYWORDS = [
    "ransomware","SonicWall","VPN","Akira","SharePoint","Microsoft",
    "CVE-","exploit","patch","LockBit","Warlock","Qilin"
]

files = sorted(glob.glob("data/raw/rss_*.csv"))
if not files:
    raise SystemExit("No raw files found. Run the collector first.")
latest = files[-1]
df = pd.read_csv(latest).fillna("")
df["when"] = df["published"].astype(str)

out_lines = [f"# Spike Explanations — derived from {latest}"]
for kw in KEYWORDS:
    m = df[(df["title"].str.contains(kw, case=False)) | (df["summary"].str.contains(kw, case=False))]
    if m.empty:
        continue
    m = m.drop_duplicates(subset=["link"]).head(8)[["source","title","link","when"]]
    out_lines.append(f"\n## {kw}")
    for _, r in m.iterrows():
        out_lines.append(f"- **{r['title']}** — {r['source']} ({r['when']}) — {r['link']}")

Path("reports/sections").mkdir(parents=True, exist_ok=True)
ts = datetime.now().strftime("%Y-%m-%d")
outf = Path(f"reports/sections/{ts}-spike-explanations.md")
with open(outf, "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
print(f"Wrote {outf}")
