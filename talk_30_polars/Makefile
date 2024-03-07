data: data/flights.csv.zip data/airports.csv data/danube.csv data/danube.dfs0

data/flights.csv.zip data/airports.csv:
	python scripts/get_data.py

data/danube.csv: data/danube.parquet
	python scripts/danube.py

data/danube.dfs0: data/danube.parquet
	python scripts/danube.py

preview:
	quarto preview polars.qmd

clean:
	rm -rf data/*.zip
	rm -rf data/*.csv
	rm -rf data/*.dfs0
	rm -f *.html
	rm -f *.ipynb
	rm -rf *_files/