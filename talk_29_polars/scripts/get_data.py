from pathlib import Path
from nycflights13 import flights

# create data directory
Path("data").mkdir(exist_ok=True)

flights.to_csv("data/flights.csv.zip", index=False, compression="gzip")