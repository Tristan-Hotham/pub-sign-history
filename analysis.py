"""What British pub names remember.

Input: data/raw/osm_pubs_churches.json.gz — OpenStreetMap amenity=pub and Christian places of worship for Great Britain,
downloaded via the Overpass API (rows: key, type P/C, lat, lon, name, old_name, denomination, building, historic,
heritage, start_date, dedication, addr). This script uses the pubs (type P).

Output: results/ tables and data/pubs.json for the web page.
"""
import gzip, json, re, sys
import numpy as np, pandas as pd, geopandas as gpd
from names import norm, ALIAS, theme

rows = json.load(gzip.open('data/raw/osm_pubs_churches.json.gz', 'rt'))
P = pd.DataFrame([r for r in rows if r[1] == 'P'], columns=['key', 't', 'lat', 'lon', 'name', 'old_name', 'denom', 'building',
                                                          'historic', 'heritage', 'start', 'dedication', 'addr'])
P = P[P.name.str.strip() != ''].copy()
P['n'] = P.name.map(norm).map(lambda s: ALIAS.get(s, s))
P = P[P.n != ''].copy()

counties = gpd.read_file('data/raw/counties.geojson')[['county', 'nation', 'geometry']]
g = gpd.GeoDataFrame(P, geometry=gpd.points_from_xy(P.lon, P.lat), crs=4326)
g = gpd.sjoin(g, counties, how='left', predicate='within').drop(columns='index_right')
g = g[g.county.notna()].copy()
P = pd.DataFrame(g.drop(columns='geometry'))
print('pubs in GB with names', len(P), file=sys.stderr)

top = P.n.value_counts()
P['theme'] = P.n.map(theme)

# distinctiveness: location quotient of each common name by county (smoothed)
common = top[top >= 40].index
cty = P.groupby('county').size()
tab = P[P.n.isin(common)].groupby(['n', 'county']).size().unstack(fill_value=0)
share_all = top[common] / len(P)
lq = (tab.div(cty, axis=1)).div(share_all, axis=0)
# most over-represented common name per county (needs at least 5 pubs of that name in the county)
dist = []
for c in tab.columns:
    s = lq[c][tab[c] >= 5].sort_values(ascending=False)
    if len(s):
        dist.append({'county': c, 'name': s.index[0], 'count': int(tab.loc[s.index[0], c]), 'lq': round(float(s.iloc[0]), 2),
                     'second': s.index[1] if len(s) > 1 else None})
dist = pd.DataFrame(dist)

# theme shares by nation and county
th = P.groupby(['nation', 'theme']).size().unstack(fill_value=0)
th_share = th.div(P.groupby('nation').size(), axis=0) * 100

# renamed pubs: old_name recorded
ren = P[P.old_name.str.strip() != ''].copy()
ren['old_n'] = ren.old_name.map(norm).map(lambda s: ALIAS.get(s, s))
ren = ren[ren.old_n != ren.n]
ren_from = ren.old_n.value_counts().head(30)
ren_theme_from = ren.old_n.map(theme).value_counts(normalize=True) * 100
ren_theme_to = ren.n.map(theme).value_counts(normalize=True) * 100

out = {
    'n_pubs': int(len(P)), 'n_names': int(P.n.nunique()),
    'share_unique': round(float((top == 1).sum() / len(P) * 100), 1),
    'top': [[k, int(v)] for k, v in top.head(60).items()],
    'themes_nation': th_share.round(2).to_dict(),
    'distinct': json.loads(dist.to_json(orient='records')),
    'renamed': {'n': int(len(ren)), 'from': [[k, int(v)] for k, v in ren_from.items()],
                'theme_from': ren_theme_from.round(1).to_dict(), 'theme_to': ren_theme_to.round(1).to_dict()},
}
json.dump(out, open('results/summary.json', 'w'), indent=1, ensure_ascii=False)
json.dump(out, open('data/summary.json', 'w'), ensure_ascii=False)
top.rename('pubs').to_csv('results/name_counts.csv', index_label='name')
dist.to_csv('results/most_distinctive_by_county.csv', index=False)

# web data: every pub as [lat, lon, name index], names list, plus per-name county counts for the top 300 names
names = list(top.index)
idx = {n: i for i, n in enumerate(names)}
clist = sorted(P.county.unique()); cidx = {c: i for i, c in enumerate(clist)}
pts = [[round(a, 4), round(b, 4), idx[n], cidx[c]] for a, b, n, c in zip(P.lat, P.lon, P.n, P.county)]
web = {'names': names, 'counts': [int(v) for v in top.values], 'pts': pts, 'distinct': json.loads(dist.to_json(orient='records')),
       'counties': clist, 'county_n': [int(cty[c]) for c in clist],
       'themes': {n: theme(n) for n in names[:400]}}
json.dump(web, open('data/pubs.json', 'w'), separators=(',', ':'), ensure_ascii=False)
print(json.dumps({k: out[k] for k in ['n_pubs', 'n_names', 'share_unique']}), file=sys.stderr)
print(top.head(40).to_string())
print(dist.sort_values('lq', ascending=False).to_string())
print(th_share.round(1).T.to_string())
print('renamed', len(ren)); print(ren_from.head(20).to_string())
print(pd.DataFrame({'from': ren_theme_from, 'to': ren_theme_to}).round(1).to_string())
