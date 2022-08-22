# %% [markdown]
# # Example project work, refactored
#
# Now with functions...

# %%
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mikeio
import tsod
import fmskill

# %%
fldr = (Path(__file__).parent.parent / "data").resolve()
save_png = False

# %% [markdown]
# ## 1. Plot stations on map

# %%
def get_stations(fldr) -> pd.DataFrame:
    """Read stations from file and return as DataFrame"""
    stations = (
        pd.read_csv(
            fldr / "obs" / "observation_positions.xyz",
            sep="\t",
            names=["lon", "lat", "z", "name"],
        )
        .set_index("name")
        .drop(columns=["z"])
    )
    return stations


# %%
def plot_mesh_and_stations(domain, stations, save_png=False):
    """Plot stations on mesh, optionally save to png"""
    domain.plot.mesh()
    for name, row in stations.iterrows():
        plt.plot(row.lon, row.lat, marker="*", markersize=10)
        plt.text(row.lon + 0.2, row.lat, name)
        plt.title("Model domain with observation stations")
    if save_png:
        plt.savefig("domain_with_stations.png")
    return plt.gca()


# %%
stations = get_stations(fldr)
station_names = stations.index
stations

# %%
domain = mikeio.Mesh(fldr / "input" / "SouthernNorthSea.mesh")
plot_mesh_and_stations(domain, stations, save_png=save_png)

# %% [markdown]
# ## 2. Load observations and remove outliers

# %%
observations = {}
for stn in station_names:
    observations[stn] = mikeio.read(fldr / "obs" / f"{stn}.dfs0").to_dataframe()

# %%
observations.keys()

# %% [markdown]
# Our outlier detector will mark an observation as an outlier if:
#
# * Value is out of range [0, 10] - non-physical values
# * The gradient is too large (single outliers)

# %%
def get_anomaly_detector(min_Hm0=0.0, max_Hm0=10.0, max_Hm0_change_per_hour=3.0):
    """tsod anomaly detector using Range and MaxGradientDetector"""
    detector = tsod.CombinedDetector(
        [
            tsod.RangeDetector(min_Hm0, max_Hm0),
            tsod.GradientDetector(max_gradient=max_Hm0_change_per_hour / 3600),
        ]
    )
    return detector


# %%
detector = get_anomaly_detector()
detector

# %% [markdown]
# Apply outlier detector for all observation series

# %%
def detect_and_remove_outliers(detector, stn, df, plot=False):
    """Remove outliers, optionally plot timeseries showing outliers"""
    anomalies = detector.detect(df.Hm0)
    n_anomalies = anomalies.sum()
    if plot:
        plt.plot(df)
        plt.plot(df[anomalies], "ro", label="Anomaly")
        plt.title(f"{stn} with {n_anomalies} outliers found")
        plt.gcf().autofmt_xdate()
        plt.show()
    df[anomalies.values] = np.nan  # remove outliers


# %%
for stn, df in observations.items():
    detect_and_remove_outliers(detector, stn, df, plot=True)
    if save_png:
        plt.savefig(f"Outliers_{stn}.png")

# %% [markdown]
# ## 3. Compare with models

# %%
def compare_single_obs_mr(fldr, observations, sim="sim1", stn="F16"):
    """Compare observation and ModelResult using FMskill"""
    fn = str(fldr / sim / "ts_significant_wave_height.dfs0")
    mr = fmskill.ModelResult(fn, item=f"{stn}: Sign. Wave Height", name=f"{sim}")
    obs = fmskill.PointObservation(observations[stn], name=f"{stn}")
    obs.itemInfo = mikeio.ItemInfo(mikeio.EUMType.Significant_wave_height)
    return fmskill.Connector(obs, mr).extract()


# %%
def compare_all(fldr, stations, observations):
    """Compare all observations with all modelresults using FMskill"""
    sim_folders = list(fldr.glob("sim*"))
    sims = [s.name for s in sim_folders]
    count = 0
    for sim in sims:
        for stn in stations.index:
            c = compare_single_obs_mr(fldr, observations, sim=sim, stn=stn)
            cc = c if count == 0 else cc + c
            count += 1
    return cc


# %%
cc = compare_all(fldr, stations, observations)
sims = cc.mod_names

# %%
cc.skill().round(3)

# %%
for stn in station_names:
    cc[stn].plot_timeseries(figsize=(10, 5))
    plt.legend(loc="upper left")
    if save_png:
        plt.savefig(f"Timeseries_comparison_{stn}.png")

# %% [markdown]
# ## 4. Find best model

# %%
meanskill = cc.mean_skill()
meanskill.round(3)

# %%
meanskill.plot_bar("rmse", title="Mean skill RMSE")
plt.ylabel("Hm0 [m]")

# %%
