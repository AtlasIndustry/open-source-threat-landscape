import feedparser, pandas as pd, time
from pathlib import Path

FEEDS = [
    "https://www.ncsc.gov.uk/section/keep-up-to-date/rss.xml",
    "https://www.cisa.gov/news-events/cybersecurity-advisories/alerts.xml",
    "https://www.krebsonsecurity.com/feed/"
]

outdir = Path("data/raw")
outdir.mkdir(parents=True, exist_ok=True)

rows = []
for url in FEEDS:
    d = feedparser.parse(url)
    for e in d.entries:
        rows.append({
            "source": d.feed.get("title", url),
            "title": e.get("title"),
            "link": e.get("link"),
            "published": e.get("published", ""),
            "summary": e.get("summary", "")
        })

df = pd.DataFrame(rows)
ts = time.strftime("%Y-%m-%d")
outfile = outdir / f"rss_{ts}.csv"
df.to_csv(outfile, index=False)
print(f"Saved {len(df)} items to {outfile}")
