import mikeio
import sys

filename = sys.argv[1]

dfs = mikeio.open(filename)

for item in dfs.items:
    print(f"* {item.name} ({item.unit.name})")
