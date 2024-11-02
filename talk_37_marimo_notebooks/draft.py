import marimo

__generated_with = "0.9.14"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        """
        ## Model skill evaluation

        The observations will be compared to observed data at the [Euro Platform](https://www.windopzee.net/meet-locaties/europlatform/)
        """
    )
    return


@app.cell
def __(mo):
    tiles = mo.ui.dropdown(["cartodb positron","openstreetmap","Stadia.StamenWatercolor"], value="cartodb positron")
    mo.md(f"Tiles: {tiles}")    
    return (tiles,)


@app.cell
def __(folium, locs, tiles):
    m = folium.Map(location=[52, 3], zoom_start=6, tiles=tiles.value)
    folium.Polygon(locs, fill_color='black', tooltip="Model domain").add_to(m)
    folium.Marker(location= [52, 3.28], tooltip="EuroPlatform").add_to(m)

    m
    return (m,)


@app.cell
def __(c):
    c.plot.timeseries(backend="plotly");
    return


@app.cell
def __(c):
    c.skill(metrics=["bias", "rmse","r2", "si"]).style(decimals=2)
    return


@app.cell
def __(c):
    c.scatter(backend="plotly")
    return


@app.cell
def __(c):
    c.plot.taylor(normalize_std=True, title="", figsize=(4,4))
    return


@app.cell
def __(mikeio):
    dfs = mikeio.open("data/HKZN_local_2017_DutchCoast.dfsu")
    dfs.geometry.boundary_polylines.exteriors[0].xy.shape

    locs = [(p[1], p[0]) for p in dfs.geometry.boundary_polylines.exteriors[0].xy]
    return dfs, locs


@app.cell
def __(mikeio, modelskill):
    fn_mod = 'data/ts_storm_4.dfs0'
    fn_obs = 'data/eur_Hm0.dfs0'
    df_mod = mikeio.read(fn_mod, items=0).to_dataframe()
    c = modelskill.match(fn_obs, fn_mod, mod_item=0, gtype='point')
    c
    return c, df_mod, fn_mod, fn_obs


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __():
    import mikeio 
    import modelskill
    import folium
    return folium, mikeio, modelskill


if __name__ == "__main__":
    app.run()
