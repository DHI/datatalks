#!/usr/bin/env python
from datetime import datetime
from enum import Enum
from typing import Annotated, Optional, List
from pathlib import Path
import json
import typer
from rich.console import Console
from rich.table import Table

import mikeio
import mikeio.generic as mg


app = typer.Typer(add_completion=False)
console = Console()


class OutputFormat(str, Enum):
    raw = "raw"
    json = "json"
    table = "table"


@app.command()
def list(path: Path, format: OutputFormat = OutputFormat.raw):

    if not path.exists():
        typer.echo(f"File does not exist: {path}")
        raise typer.Exit(code=1)

    dfs = mikeio.open(path)
    start_time = dfs.time[0]
    end_time = dfs.time[-1]
    print(f"File: {path} ({start_time} - {end_time})")

    if format == OutputFormat.raw:
        for item in dfs.items:
            print(f"* {item.name} ({item.unit.name})")
    elif format == OutputFormat.json:
        res = []
        for item in dfs.items:
            res.append({"name": item.name, "unit": item.unit.name})
        print(json.dumps(res, indent=2))
    elif format == OutputFormat.table:
        table = Table("Name", "Unit")
        for item in dfs.items:
            table.add_row(item.name, item.unit.name)
        console.print(table)



@app.command()
def extract(
    infilename: str,
    outfilename: str,
    item: Optional[List[str]] = typer.Option(None,"---item", "-i",help="Item name, default is all items") ,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
):
    """Extract a subset of a dfs file"""
    mg.extract(
        infilename=infilename,
        outfilename=outfilename,
        items=item,
        start=start,
        end=end,
    )


if __name__ == "__main__":
    app()
