# What pub names remember

**Read the post and map any pub name:** https://tristan-hotham.github.io/pub-sign-history/

**Archived data and code:** [doi:10.5281/zenodo.23676495](https://doi.org/10.5281/zenodo.23676495)

This project takes every named pub in Great Britain in OpenStreetMap, groups the pubs by name and maps them. It asks which histories pub signs still carry, and which names give a county away.

## Findings

- There are 37,559 named pubs and 16,349 different names. 36% of pubs have a name no other pub shares.
- The commonest names are the Red Lion (531), Crown (450), Royal Oak (405), White Hart (298), Plough (274), Swan and White Horse (262 each) and Railway (261).
- Some names give a county away. Each county's most over-represented common name (40 or more pubs nationally, 5 or more in the county) is listed in `results/most_distinctive_by_county.csv`. Examples are the Black Lion in Dyfed (15× the national rate), the Talbot in Worcestershire (14×), the Cricketers in Surrey (11×), the Black Bull in Northumberland (11×), the Miners Arms in Derbyshire (9×) and the Bay Horse in North Yorkshire (9×).
- Traditional themed names are much commoner in England (41% of pubs) and Wales (34%) than in Scotland (16%).
- Former names recorded in OpenStreetMap (1,103 pubs) include 1990s and 2000s chain brands such as Hobgoblin, Tap and Spile, Last Orders, O'Neill's and Varsity.

## Method

1. Pubs are all features tagged `amenity=pub` with a name, downloaded through the Overpass API on 26 October 2026 in 1.2° × 1.6° tiles.
2. Names are lower-cased and stripped of "The", "Ye Olde" and trailing Inn, Hotel, Tavern or Pub. A few variants are merged (see `names.py`).
3. Each pub is assigned to a ceremonial county (England), preserved county (Wales) or council area (Scotland).
4. Distinctiveness is the location quotient: a name's share of a county's pubs divided by its share nationally.
5. Themes come from a rough keyword grouping in `names.py`. They are a guide, not a classification.

## Files

| Path | What it is |
|---|---|
| `analysis.py`, `names.py` | Analysis and name normalisation |
| `data/raw/osm_pubs_churches.json.gz` | OpenStreetMap extract: pubs and Christian places of worship in Great Britain. Each row holds key, type (P/C), lat, lon, name, old_name, denomination, building, historic, heritage, start_date, dedication, addr. The churches are used in the companion project [saints-geography](https://github.com/Tristan-Hotham/saints-geography). |
| `data/raw/counties.geojson` | Counties built from ONS 2025 local authority boundaries |
| `results/name_counts.csv` | Every normalised name with its number of pubs |
| `results/most_distinctive_by_county.csv` | The most over-represented common name per county |
| `results/summary.json` | Headline figures, theme shares by nation and renamed pubs |
| `index.html`, `data/` | The web page and its data |

## Sources and licences

- Pubs and churches: © OpenStreetMap contributors. The extract in `data/raw/` and the derived pub data are available under the Open Database Licence (ODbL).
- Boundaries: Office for National Statistics, Open Government Licence v3. Contains OS data © Crown copyright and database right.
- Base map: © Esri.

Code is MIT licensed.

AI use: written with drafting, data and coding help from Claude (Anthropic).

Tristan Hotham, independent researcher, 2026.
