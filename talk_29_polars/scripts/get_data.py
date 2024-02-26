from pathlib import Path
from nycflights13 import flights, airports, airlines, weather

# create data directory
Path("data").mkdir(exist_ok=True)

flights.to_csv("data/flights.csv.zip", index=False, compression="gzip")
airports.to_csv("data/airports.csv", index=False)