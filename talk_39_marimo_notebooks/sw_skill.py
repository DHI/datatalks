import marimo

__generated_with = "0.10.15"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ## Model skill evaluation

        The observations will be compared to observed data at the [Euro Platform](https://www.windopzee.net/meet-locaties/europlatform/)
        """
    )
    return


@app.cell
def _(modelskill):
    c = modelskill.match(obs='data/eur_Hm0.dfs0',mod='data/ts_storm_4.dfs0', mod_item=0, gtype='point')
    c
    return (c,)


@app.cell
def _(mikeio):
    dfs = mikeio.open("data/HKZN_local_2017_DutchCoast.dfsu")
    dfs.geometry.boundary_polylines.exteriors[0].xy.shape

    locs = [(p[1], p[0]) for p in dfs.geometry.boundary_polylines.exteriors[0].xy]
    return dfs, locs


@app.cell
def _(mo):
    tiles = mo.ui.dropdown(["cartodb positron","openstreetmap","Stadia.StamenWatercolor"], value="cartodb positron", label="Tiles")
    tiles
    return (tiles,)


@app.cell
def _(folium, locs, tiles):
    m = folium.Map(location=[52, 3], zoom_start=6, tiles=tiles.value)
    folium.Polygon(locs, fill_color='black', tooltip="Model domain").add_to(m)
    folium.Marker(location= [52, 3.28], tooltip="EuroPlatform").add_to(m)

    m
    return (m,)


@app.cell
def _(c):
    ts = c.plot.timeseries(backend="plotly");
    ts
    return (ts,)


@app.cell
def _(c, skill_metrics):
    sk = c.skill(metrics=skill_metrics.value).style(decimals=2)
    sk
    return (sk,)


@app.cell
def _(mo):
    skill_metrics = mo.ui.multiselect(["bias","rmse", "mae", "kge", "cc", "si", "r2"], value=["bias", "r2"], label="Metrics")
    skill_metrics
    return (skill_metrics,)


@app.cell
def _(c):
    tay = c.plot.taylor(normalize_std=True, title="", figsize=(4,4))
    tay
    return (tay,)


@app.cell
def _(c):
    sc = c.plot.scatter(backend="plotly")
    sc
    return (sc,)


@app.cell
def _(m, mo, sk, tay, ts):
    mo.ui.tabs({"Map":m,"Timeseries": ts, "Skill": sk, "Taylor":tay})
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import mikeio 
    import modelskill
    import folium
    return folium, mikeio, modelskill


if __name__ == "__main__":
    app.run()
