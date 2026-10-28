"""r/dataisbeautiful collage for pub-sign-history: what_pub_names_remember.png (2400 x 3000).
Every number is read from the project's results (results/summary.json, results/most_distinctive_by_county.csv) or
computed from data/pubs.json. Run: python3 collage.py  (PUBS=/path/to/pub-sign-history to point elsewhere)
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
PUBS = os.environ.get("PUBS", "/home/claude/pubs"); sys.path.insert(0, PUBS)
import numpy as np, pandas as pd
from house import *
from names import theme
from matplotlib.patches import Rectangle

S = json.load(open(os.path.join(PUBS, "results/summary.json")))
DIST = pd.read_csv(os.path.join(PUBS, "results/most_distinctive_by_county.csv"))
NC = pd.read_csv(os.path.join(PUBS, "results/name_counts.csv")) if os.path.exists(os.path.join(PUBS, "results/name_counts.csv")) else None
D = json.load(open(os.path.join(PUBS, "data/pubs.json")))
C = counties_km(os.path.join(PUBS, "data/raw/counties.geojson"))

TH = {"Heraldry and great families": "#C38B2C", "Crown and monarchy": "#9B2C3F", "Animals and sport": "#2E8C86",
      "Farming and trades": "#6A8F3A", "Roads, rails and canals": "#2F6690", "Faith and pilgrimage": "#7B5AA6",
      "War and heroes": "#8A5A3C", None: "#BDB3A2"}
SHORT = {"Heraldry and great families": "heraldry, great families", "Crown and monarchy": "crown and monarchy",
         "Animals and sport": "animals and sport", "Farming and trades": "farming and trades",
         "Roads, rails and canals": "roads, rails, canals", "Faith and pilgrimage": "faith and pilgrimage",
         "War and heroes": "war and heroes", None: "other names"}
title = lambda s: " ".join(w if w in ("and", "of", "the", "in") else w.capitalize() for w in s.split())

N, NN, UNIQ = S["n_pubs"], S["n_names"], S["share_unique"]
top = S["top"]
tn = {n: sum(S["themes_nation"][t][n] for t in S["themes_nation"]) for n in ("England", "Scotland", "Wales")}
DIST["theme"] = [theme(n) for n in DIST.name]; DIST["theme"] = DIST.theme.astype(object).where(DIST.theme.notna(), None)
DIST = DIST.set_index("county")
best = DIST.sort_values("lq", ascending=False)

fig = new_fig()
x = words(fig, 0.045, 0.972, [("Which", FG), ("pub name", TH["Crown and monarchy"]), ("gives", FG)])
words(fig, 0.045, 0.924, [("your", FG), ("county", TH["Heraldry and great families"]), ("away?", FG)])
fig.text(0.045, 0.862, f"All {N:,} named pubs in Great Britain on OpenStreetMap. Each county is coloured by the theme of\n"
         "the common pub name most over-represented there, against its share of pubs across Britain.",
         family=SER, fontsize=14.5, color=FG, va="top", linespacing=1.15)

# hero map
ax = fig.add_axes([0.0, 0.25, 0.57, 0.56]); ax.set_facecolor(BGC)
col = [TH.get(DIST.theme[c], TH[None]) if c in DIST.index else LAND for c in C.county]
C.plot(ax=ax, color=col, edgecolor=BGC, linewidth=0.6, zorder=1)
ax.set_xlim(125, 660); ax.set_ylim(5, 735); ax.set_aspect(1); ax.axis("off")
# labels: counties where the name is at least 7 times its national share; a few nudged
nudge = {"Durham": (40, -6), "South Yorkshire": (22, -4), "Clwyd": (-38, 14), "Cumbria": (-8, 0), "Cambridgeshire": (12, 0),
         "Leicestershire": (14, 0), "Warwickshire": (-4, -8), "Staffordshire": (-6, 6), "Derbyshire": (2, 4), "Oxfordshire": (-6, 0),
         "Bedfordshire": (8, -4), "Powys": (-4, 4), "Worcestershire": (-2, -4), "Northumberland": (-4, 4)}
for c, g in zip(C.county, C.geometry):
    if c not in DIST.index or DIST.lq[c] < 7: continue
    p = g.representative_point(); dx, dy = nudge.get(c, (0, 0))
    tx, ty = p.x + dx, p.y + dy
    if abs(dx) + abs(dy) > 30:
        ax.plot([p.x, tx], [p.y, ty], color=FG, lw=.6, zorder=3)
    ax.text(tx, ty, f"{title(DIST.name[c])}\n{DIST.lq[c]:.0f}×", family=MONO, fontsize=10, color=FG, ha="center", va="center",
            zorder=4, linespacing=1.0, path_effects=halo(2.6))

# key
fig.text(0.6, 0.795, "THEME OF THE NAME", family=MONO, fontsize=11, color=MUT)
for i, (t, c) in enumerate(TH.items()):
    r, k = divmod(i, 2)
    xx, yy = 0.6 + k * 0.205, 0.768 - r * 0.026
    fig.patches.append(Rectangle((xx, yy - 0.004), 0.016, 0.0128, transform=fig.transFigure, color=c))
    fig.text(xx + 0.022, yy + 0.002, SHORT[t], family=MONO, fontsize=9.6, color=FG, va="center")
fig.text(0.6, 0.662, "Labels: the name, and how many times its share\nof pubs in Britain (7× or more). Grey: no\nrepeated name stands out (most of Scotland).", family=MONO,
         fontsize=9.2, color=MUT, va="top", linespacing=1.3)

# headline numbers
pw = best.iloc[0]; s2, s3 = best.iloc[1], best.iloc[2]
items = [
    (f"{top[0][1]}", TH["Heraldry and great families"],
     f"pubs are called the {title(top[0][0])}, Britain's commonest\nname, ahead of the {title(top[1][0])} ({top[1][1]}) and the\n{title(top[2][0])} ({top[2][1]})."),
    (f"{UNIQ:.0f}%", TH["Roads, rails and canals"],
     f"of pubs have a name no other pub shares:\n{NN:,} different names for {N:,} pubs."),
    (f"{pw.lq:.0f}×", TH["Animals and sport"],
     f"as common in {pw.name} as across Britain: the\n{title(pw['name'])}. Next come the {title(s2['name'])} in {s2.name}\n({s2.lq:.0f}×) and the {title(s3['name'])} in {s3.name} ({s3.lq:.0f}×)."),
    (f"{tn['England']:.0f}% v {tn['Scotland']:.0f}%", TH["Crown and monarchy"],
     f"of pubs with a traditional themed name in\nEngland and in Scotland. Wales: {tn['Wales']:.0f}%."),
]
headlines(fig, [0.6, 0.245, 0.39, 0.36], items, big=36, step=0.255, sub_off=0.105)

# bottom strip: the twelve commonest names
label(fig, 0.045, 0.238, "THE TWELVE COMMONEST PUB NAMES IN GREAT BRITAIN")
mx = top[0][1]
for k in range(2):
    a = fig.add_axes([0.2 + k * 0.47, 0.085, 0.27, 0.14]); a.axis("off"); a.set_facecolor(BGC)
    sub = top[k * 6:(k + 1) * 6]
    for i, (n, v) in enumerate(sub):
        y = 5 - i
        a.barh(y, v, height=.68, color=TH[theme(n)])
        a.text(-12, y, title(n), family=SER, fontsize=12.5, color=FG, ha="right", va="center")
        a.text(v + 8, y, f"{v}", family=MONO, fontsize=10.5, color=MUT, va="center")
    a.set_xlim(0, mx * 1.12); a.set_ylim(-.6, 5.6)

footer(fig, f"Data: © OpenStreetMap contributors (ODbL), every amenity=pub with a name, downloaded 26 October 2026. Counties from ONS 2025\n"
       "boundaries (OGL v3). Names normalised (no 'The', 'Inn', 'Hotel'); over-representation needs 40+ pubs in Britain and 5+ in the\n"
       "county. Themes are a rough keyword grouping. Analysis and chart: Tristan Hotham, with Python and matplotlib.")
fig.savefig(os.path.join(HERE, "what_pub_names_remember.png"), dpi=200, facecolor=BGC)
print("written")
