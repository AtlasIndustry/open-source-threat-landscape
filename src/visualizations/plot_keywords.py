import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv("data/processed/keyword_counts.csv", index_col=0)
ax = df.plot(kind="bar", legend=False, title="Keyword Frequency (Open-Source Feeds)")
plt.tight_layout()
Path("visualizations").mkdir(parents=True, exist_ok=True)
plt.savefig("visualizations/keyword_freq.png")
print("Saved visualizations/keyword_freq.png")
