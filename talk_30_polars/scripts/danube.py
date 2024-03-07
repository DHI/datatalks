import polars as pl
import mikeio

df = pl.read_parquet("data/danube.parquet")
df.write_csv("data/danube.csv")

df_pd = df.to_pandas().set_index("date")
df_pd.to_dfs0("data/danube.dfs0")
