import feedparser, pandas as pd, time
from pathlib import Path

DAYS_BACK = 21

FEEDS = [
    "https://www.cisa.gov/news-events/cybersecurity-advisories/alerts.xml",
    "https://www.cisa.gov/news-events/ics-advisories/ics-advisories.xml",
    "https://www.ncsc.gov.uk/section/keep-up-to-date/rss.xml",
    "https://isc.sans.edu/rssfeed.xml",

    "https://msrc.microsoft.com/blog/feed/",
    "https://security.googleblog.com/atom.xml",
    "https://googleprojectzero.blogspot.com/feeds/posts/default?alt=rss",
    "https://blog.talosintelligence.com/feeds/posts/default",      
    "https://unit42.paloaltonetworks.com/feed/",                   
    "https://www.crowdstrike.com/blog/feed/",
    "https://www.mandiant.com/resources/blog/rss.xml",
    "https://securelist.com/feed/",                                
    "https://www.welivesecurity.com/feed/",                      
    "https://nakedsecurity.sophos.com/feed/",
    "https://blog.malwarebytes.com/feed/",
    "https://research.checkpoint.com/feed/",
    "https://www.proofpoint.com/us/blog/threat-insight/feed",
    "https://www.rapid7.com/blog/feed/",
    "https://blog.qualys.com/feed",
    "https://blogs.vmware.com/security/feed/",

    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.securityweek.com/feed/",

    "https://www.exploit-db.com/rss.xml",
    "https://rss.packetstormsecurity.com/files/",
    "https://seclists.org/rss/fulldisclosure.rss",

    "https://www.reddit.com/r/netsec/.rss",
    "https://www.reddit.com/r/cybersecurity/.rss",
    "https://riskybiznews.substack.com/feed",
]

def best_summary(entry):
    for k in ("summary", "description"):
        if entry.get(k):
            return entry[k]
    if entry.get("content") and isinstance(entry["content"], list) and entry["content"]:
        return entry["content"][0].get("value", "")
    return ""

cutoff_ts = time.time() - (DAYS_BACK * 24 * 60 * 60)

outdir = Path("data/raw"); outdir.mkdir(parents=True, exist_ok=True)
rows = []

for url in FEEDS:
    try:
        d = feedparser.parse(url)
        entries = getattr(d, "entries", []) or []
        if not entries:
            continue
        for e in entries:
            pub_ts = None
            if e.get("published_parsed"):
                pub_ts = time.mktime(e.published_parsed)
            if pub_ts is None or pub_ts >= cutoff_ts:
                rows.append({
                    "source": d.feed.get("title", url),
                    "title": e.get("title", ""),
                    "link": e.get("link", ""),
                    "published": e.get("published", ""),
                    "summary": best_summary(e),
                })
    except Exception as ex:
        print(f"[skip] {url}: {ex}")

df = pd.DataFrame(rows)

if not df.empty:
    df.drop_duplicates(subset=["link"], inplace=True)

stamp = time.strftime("%Y-%m-%dT%H%M%S")
outfile = outdir / f"rss_{stamp}.csv"
df.to_csv(outfile, index=False)
print(f"Saved {len(df)} items to {outfile}")
