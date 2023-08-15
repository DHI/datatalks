#!/usr/bin/env python
from datetime import datetime
from typing import Optional
import typer
import mikeio
import mikeio.generic as mg

app = typer.Typer(add_completion=False)


@app.command()
def list(filename: str):
    dfs = mikeio.open(filename)
    start_time = dfs.time[0]
    end_time = dfs.time[-1]
    print(f"File: {filename} ({start_time} - {end_time})")

    for item in dfs.items:
        print(f"* {item.name} ({item.unit.name})")


@app.command()
def extract(
    infilename: str,
    outfilename: str,
    item: Optional[str] = None,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
):
    """Extract a subset of a dfs file
    
    The default is to extract all items and all time steps.
    """
    mg.extract(
        infilename=infilename,
        outfilename=outfilename,
        items=item,
        start=start,
        end=end,
    )


if __name__ == "__main__":
    app()
