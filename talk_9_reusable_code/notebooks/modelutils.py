import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mikeio
import tsod
import fmskill


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


def plot_mesh_and_stations(domain, stations, save_png=False):
    """Plot stations on mesh

    Parameters
    ----------
    mesh : _type_
        _description_
    stations : _type_
        _description_
    save_png : bool, optional
        _description_, by default False
    """
    domain.plot.mesh()
    for name, row in stations.iterrows():
        plt.plot(row.lon, row.lat, marker="*", markersize=10)
        plt.text(row.lon + 0.2, row.lat, name)
        plt.title("Model domain with observation stations")
    # plt.savefig()
    return plt.gca()


def get_anomaly_detector(
    min_Hm0=0.0, max_Hm0=10.0, max_Hm0_change_per_hour=3.0
) -> tsod.CombinedDetector:
    """tsod anomaly detector using Range and MaxGradientDetector

    Parameters
    ----------
    min_Hm0 : float, optional
        Minimum allowed value, by default 0.0
    max_Hm0 : float, optional
        Maximum allowed value, by default 10.0
    max_Hm0_change_per_hour : float, optional
        Maximum allowed gradient, by default 3.0

    Returns
    -------
    tsod.CombinedDetector
        A combined detector
    """
    detector = tsod.CombinedDetector(
        [
            tsod.RangeDetector(min_Hm0, max_Hm0),
            tsod.GradientDetector(max_gradient=max_Hm0_change_per_hour / 3600),
        ]
    )
    return detector


def detect_and_remove_outliers(
    detector: tsod.CombinedDetector, stn: str, df: pd.DataFrame, plot=False
) -> pd.DataFrame:
    anomalies = detector.detect(df.Hm0)
    n_anomalies = anomalies.sum()
    if plot:
        plt.plot(df)
        plt.plot(df[anomalies], "ro", label="Anomaly")
        plt.title(f"{stn} with {n_anomalies} outliers found")
        plt.gcf().autofmt_xdate()
        plt.show()
    df[anomalies.values] = np.nan  # remove outliers
    return df


def _compare_single_obs_mr(
    fldr, observations, sim="sim1", stn="F16"
) -> fmskill.comparison.ComparerCollection:
    fn = str(fldr / sim / "ts_significant_wave_height.dfs0")
    mr = fmskill.ModelResult(fn, item=f"{stn}: Sign. Wave Height", name=f"{sim}")
    obs = fmskill.PointObservation(observations[stn], name=f"{stn}")
    obs.itemInfo = mikeio.ItemInfo(mikeio.EUMType.Significant_wave_height)
    return fmskill.Connector(obs, mr).extract()


def compare_all(fldr, stations, observations):
    sim_folders = list(fldr.glob("sim*"))
    sims = [s.name for s in sim_folders]
    count = 0
    for sim in sims:
        for stn in stations.index:
            c = _compare_single_obs_mr(fldr, observations, sim=sim, stn=stn)
            cc = c if count == 0 else cc + c
            count += 1
    return cc
