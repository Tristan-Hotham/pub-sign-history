## Title

[OC] Which pub name gives your county away? The Lion is 21 times commoner in Powys than across Britain and the Talbot 14 times commoner in Worcestershire, from all 37,559 named pubs in Great Britain (OpenStreetMap)

## Body (optional)

I grouped every named pub in Great Britain on OpenStreetMap by its name: 37,559 pubs share 16,349 names, and 36% of pubs have a name no other pub has. The Red Lion is the commonest (531), ahead of the Crown (450) and the Royal Oak (405). For each county I then found the common name most over-represented there: the Lion in Powys (21×), the Black Lion in Dyfed (15×), the Talbot in Worcestershire (14×), the Station in Fife (12×), and the Cricketers in Surrey and the Black Bull in Northumberland (11× each). Traditional themed names (crown, heraldry, farming, roads and rails and so on) cover 41% of pubs in England and 34% in Wales, but only 16% in Scotland.

Caveat: OpenStreetMap is not a complete register of pubs, and the themes are a rough keyword grouping, not a classification.

Interactive version: https://tristan-hotham.github.io/pub-sign-history/

## Source comment

Source: every feature tagged amenity=pub with a name in Great Britain, downloaded from OpenStreetMap through the Overpass API on 26 October 2026 (© OpenStreetMap contributors, Open Database Licence; the extract and derived pub data are under the ODbL). Names are lower-cased and stripped of "The", "Ye Olde" and a trailing Inn, Hotel, Tavern or Pub. Over-representation is the location quotient: a name's share of a county's pubs divided by its share across Britain, for names with 40 or more pubs nationally and 5 or more in the county. Counties (ceremonial in England, preserved in Wales, council areas in Scotland) built from Office for National Statistics 2025 boundaries, Open Government Licence v3, contains OS data © Crown copyright and database right. Base map on the interactive page © Esri.

Tools: Python (pandas, NumPy, GeoPandas, pyproj, matplotlib).

Interactive: https://tristan-hotham.github.io/pub-sign-history/
Blog post: https://blog.tristanhotham.com/2026/10/26/what-pub-names-remember/
Data and code: https://doi.org/10.5281/zenodo.23676495
