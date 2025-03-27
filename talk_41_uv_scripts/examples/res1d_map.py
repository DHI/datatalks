# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "folium",
#     "geopandas",
#     "mapclassify",
#     "mikeio1d",
# ]
# ///
import sys

from pathlib import Path
import mikeio1d
import webbrowser
import time

path = Path(sys.argv[1])
if not path.exists():
    raise FileNotFoundError(path)

res = mikeio1d.open(path)
gdf = res.catchments.to_geopandas(agg='max')

map = gdf.explore(column='max_TotalRunOff', legend=True, tiles="cartodb positron", tooltip=["name", "max_TotalRunOff"], popup=True)

map_html_path = Path("temp.html")
map.save(map_html_path)

webbrowser.open(map_html_path.resolve().as_uri())

time.sleep(5)
map_html_path.unlink()
