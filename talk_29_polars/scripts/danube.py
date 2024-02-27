import polars as pl

pl.read_parquet("data/danube.parquet").write_csv("data/danube.csv")