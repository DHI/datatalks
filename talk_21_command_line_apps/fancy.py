import mikeio
import sys
import json

filename = sys.argv[1]
out_format = sys.argv[2]

dfs = mikeio.open(filename)


if out_format == "json":
    res = []
    for item in dfs.items:
        res.append({"name": item.name, "unit": item.unit.name})
    print(json.dumps(res, indent=2))

else:
    for item in dfs.items:
        print(f"* {item.name} ({item.unit.name})")