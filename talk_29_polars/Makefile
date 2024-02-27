data: data/flights.csv.zip data/airports.csv data/danube.csv

data/flights.csv.zip data/airports.csv:
	python scripts/get_data.py

data/danube.csv: data/danube.parquet
	python scripts/danube.py