## Dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

from typing import List, Dict, Tuple
from numpy.lib.npyio import NpzFile


class MFXDataAccessUtils:
    ## Functions
    @staticmethod
    def grab_file_paths(root: str, filetype: str = ".npz") -> List:
        """
        Function to grab all file paths in a directory.
        """
        return glob(f"{root}/**/*{filetype}", recursive=True)

    @staticmethod
    def is_complex_npz(data: NpzFile) -> bool:
        """
        Function to check if a .npz file is complex.
        """
        for datatype in [array.dtype for array in data.values()]:
            if datatype in [np.dtype("object"), np.dtype("O")]:
                return True
        return False

    @staticmethod
    def check_if_pickle_is_required(file: str) -> bool:
        """
        Function to check if a .npz file requires pickle to load.
        """
        try:
            out = np.load(file, allow_pickle=False)
            _ = [array for array in out.values()]
            return False
        except ValueError:
            # If a ValueError is raised, it means that the file requires pickle to load
            return True

    @staticmethod
    def load(file: str, print_keys: bool = False, allow_pickle: bool = False) -> Dict:
        """
        Function to load a .npz file. Will display the keys set in the file.
        """
        if not allow_pickle:
            if not MFXDataAccessUtils.check_if_pickle_is_required(file):
                return MFXDataAccessUtils.load_without_pickle(
                    file, print_keys=print_keys
                )
            else:
                print(f"File {file} requires pickle to load.")
                return print("Please set allow_pickle=True to load the file.")

        if not MFXDataAccessUtils.is_complex_npz(
            np.load(file, allow_pickle=allow_pickle)
        ):
            return MFXDataAccessUtils.load_without_pickle(file, print_keys=print_keys)
        else:
            return MFXDataAccessUtils.load_npz_into_separate_sets(file)

    @staticmethod
    def load_without_pickle(file: str, print_keys: bool = False) -> Dict:
        """
        Function to load a .npz file. Will display the keys set in the file.
        """
        out = np.load(file, allow_pickle=False)
        if print_keys:
            print(f"Keys in file: {out.files}")
        return {"data": out, "results": {}, "metadata": {}}

    @staticmethod
    def load_npz_into_separate_sets(file: str) -> Dict:
        """
        Function to load a .npz file into separate sets.
        """
        out = np.load(file, allow_pickle=True)

        arrays = {key: out[key] for key in out.files if all(c.isupper() for c in key)}
        results = {
            key: out[key].item()
            for key in out.files
            if any(c.islower() for c in key) and key not in ["metadata", "allow_pickle"]
        }
        metadata = out["metadata"].item() if "metadata" in out.files else {}

        return {"data": arrays, "results": results, "metadata": metadata}

    @staticmethod
    def to_matrix(data: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Function to transform a dictionairy into a matrix.
        """
        return np.stack([val for val in data.values()], axis=1)

    @staticmethod
    def to_df(data: Dict[str, np.ndarray]) -> pd.DataFrame:
        """
        Function to transform a dictionairy into a pandas DataFrame.
        """
        return pd.DataFrame({key: val for key, val in data.items()})

    @staticmethod
    def cast_to_matrix(
        data: Dict[str, np.ndarray], ignore_keys: List[str] = ["ID"]
    ) -> np.ndarray:
        """
        Function to cast a .npz file to a matrix.
        """
        return np.stack(
            [val for key, val in data.items() if key not in ignore_keys], axis=1
        ), [key for key in data if key not in ignore_keys]

    @staticmethod
    def construct_tracks_to_matrices(
        data: Dict[str, np.ndarray],
    ) -> Dict[str, np.ndarray]:
        """
        Function to extract tracks from a .npz file and return them as a dictionary of matrices.
        """

        # Extract the unique IDs. we need these to construct the tracks
        ID_arr = data.get("ID")
        un = np.unique(ID_arr).astype("uint16")

        out, _ = MFXDataAccessUtils.cast_to_matrix(data, ignore_keys=["ID"])

        return {ID: out[np.argwhere(ID_arr == ID).flatten(), :] for ID in un}

    @staticmethod
    def construct_tracks_to_dictionary(
        data: Dict[str, np.ndarray], required_keys: List[str]
    ) -> Dict[str, Dict[str, np.ndarray]]:
        # Extract the unique IDs. we need these to construct the tracks
        ID_arr = data.get("ID")
        un = np.unique(ID_arr).astype("uint16")

        out, keys = MFXDataAccessUtils.cast_to_matrix(data, ignore_keys=["ID"])

        data_dict = {ID: out[np.argwhere(ID_arr == ID).flatten(), :] for ID in un}
        return {
            ID: {
                key: data_dict[ID][:, i]
                for i, key in enumerate(keys)
                if key in required_keys
            }
            for ID in un
        }

    ## Plotting
    @staticmethod
    def overview_2d(
        data: pd.DataFrame, x: str, y: str, hue: str
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Function to plot a 2D overview of the data.
        """

        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
        img = ax.scatter(
            x=data[x],
            y=data[y],
            c=data[hue],
            alpha=0.5,
            s=3,
            cmap="magma",
            label=f"color: {hue}",
        )

        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(f"{x} vs {y}")
        fig.colorbar(mappable=img)

        fig.tight_layout()

        return fig, ax

    @staticmethod
    def show_track(
        track_dict: Dict[str, Dict[str, np.ndarray]], ID: int, x: str, y: str, hue: str
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Function to plot a track.
        """
        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
        # plot connection lines
        ax.plot(
            track_dict[ID][x],
            track_dict[ID][y],
            color="black",
            alpha=0.5,
            lw=1,
            zorder=1,
        )
        img = ax.scatter(
            x=track_dict[ID][x],
            y=track_dict[ID][y],
            c=track_dict[ID][hue],
            s=15,
            cmap="magma",
            label=f"color: {hue}",
            zorder=2,
        )

        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(f"Track {ID}")
        ax.legend()
        fig.colorbar(mappable=img)

        fig.tight_layout()

        return fig, ax

    @staticmethod
    def plot_msd(
        msd: np.ndarray,
        lags: np.ndarray,
        title: str = "Mean Squared Displacement",
        xlabel: str = "Lags [s]",
        ylabel: str = "MSD [nm²]",
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Function to plot the MSD.
        """
        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
        ax.plot(lags, msd)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        fig.tight_layout()

        return fig, ax
    
    @staticmethod
    def plot_msd_overview(
        msd_lags:Dict[int, Dict[str, np.ndarray]],
        title: str = "Mean Squared Displacement Overview",
        xlabel: str = "Lags [s]",
        ylabel: str = "MSD [nm²]",
    )-> Tuple[plt.Figure, plt.Axes]:
        """
        Function to plot the MSD overview.
        """
        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
        for ID, data in msd_lags.items():
            ax.plot(data["lags"], data["msd"])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        fig.tight_layout()

        return fig, ax

    @staticmethod
    def plot_cycle_trace(
        integrated_cycles: np.ndarray,
        dormant_cycles: np.ndarray,
        upper_limit: int,
        title: str = "Cycle Trace",
        xlabel: str = "Localization Number",
        ylabel: str = "Cycle Trace [a.u.]",
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Function to plot the cycle trace.
        """
        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
        ax.plot(integrated_cycles, label="Integrated Cycles", color="blue")
        ax.plot(dormant_cycles, label="Dormant Cycles", color="red")
        ax.axhline(y=upper_limit, color="k", linestyle="--", label="Upper Limit 1μ+1σ")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend()
        fig.tight_layout()

        return fig, ax
