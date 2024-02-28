data: data/flights.csv.zip data/airports.csv data/danube.csv data/danube.dfs0

data/flights.csv.zip data/airports.csv:
	python scripts/get_data.py

data/danube.csv: data/danube.parquet
	python scripts/danube.py

data/danube.dfs0: data/danube.parquet
	python scripts/danube.py