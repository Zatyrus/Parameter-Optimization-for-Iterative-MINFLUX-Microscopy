## Dependencies
import numpy as np
import pandas as pd

from pprint import pprint
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional
from data_tools import MFXDataAccessUtils


class Dataset:
    data: Dict
    metadata: Optional[Dict]
    results: Optional[Dict]

    def __init__(self, data: Dict, metadata: Dict, results: Dict):
        """
        Initialize the Dataset object with data, metadata, and results.

        Parameters:
        - data (Dict): The main data dictionary.
        - metadata (Optional[Dict]): Optional metadata dictionary.
        - results (Optional[Dict]): Optional results dictionary.
        """

        self.data = data
        self.metadata = metadata
        self.results = results

        self.__post_init__()

    def __post_init__(self):
        "Execute after the object is initialized"
        # Add cycle information to the data if present
        self.__add_cycle_to_data()
        # Convert the data to track format
        self.track_dict = self.get_tracks_as_dictionary(required_keys=self.data.keys())

    @classmethod
    def from_file(
        cls, file: str, print_keys: bool = False, allow_pickle: bool = False
    ) -> "Dataset":
        """
        Load a Dataset object from a file.

        Parameters:
        - file (str): The path to the file.
        - print_keys (bool): Whether to print the keys in the file.
        - allow_pickle (bool): Whether to allow loading with pickle.

        Returns:
        - Dataset: The loaded Dataset object.
        """

        data = MFXDataAccessUtils.load(
            file, print_keys=print_keys, allow_pickle=allow_pickle
        )

        return cls(**data)

    def __add_cycle_to_data(self) -> None:
        """
        Add cycle information to the data if present.
        """

        if "cycle_container" in self.results:
            cycle_container = self.results["cycle_container"]

            # setup collector
            cycle_data = {
                "CYCLES": [],
                "INTEGRATED": [],
                "DORMANT": [],
            }

            # collect and append the cycle data
            for val in cycle_container.values():
                for col_key in cycle_data.keys():
                    cycle_data[col_key].append(val.get(col_key, None))

            # concatenate the cycle data
            for key in cycle_data.keys():
                cycle_data[key] = np.concatenate(cycle_data[key], axis=0)

            ## add the cycle data to the main data
            for key in cycle_data.keys():
                if key not in self.data:
                    self.data[key] = cycle_data[key]
                else:
                    print(f"Key {key} already exists in the data. Skipping.")

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert the data to a pandas DataFrame.

        Returns:
        - pd.DataFrame: The data as a DataFrame.
        """

        return pd.DataFrame(self.data)

    def to_matrix(self) -> np.ndarray:
        """
        Convert the data to a numpy matrix.

        Returns:
        - np.ndarray: The data as a matrix.
        """

        return MFXDataAccessUtils.to_matrix(self.data)

    def to_matrix_with_labels(
        self, ignore_keys: List[str] = []
    ) -> Tuple[np.ndarray, List[str]]:
        """
        Convert the data to a numpy matrix with labels.

        Returns:
        - Tuple[np.ndarray, List[str]]: The data as a matrix and the labels.
        """

        return MFXDataAccessUtils.cast_to_matrix(self.data, ignore_keys=ignore_keys)

    def get_tracks_as_matrices(self) -> Dict[str, np.ndarray]:
        """
        Get the tracks as matrices.

        Returns:
        - Dict[str, np.ndarray]: The tracks as matrices.
        """

        return MFXDataAccessUtils.construct_tracks_to_matrices(self.data)

    def get_tracks_as_dictionary(
        self,
        required_keys: List[str] = [
            "X",
            "Y",
            "T",
            "ID",
            "ECO",
            "EFO",
        ],
    ) -> Dict[str, np.ndarray]:
        """
        Get the tracks as a dictionary.

        Returns:
        - Dict[str, np.ndarray]: The tracks as a dictionary.
        """

        return MFXDataAccessUtils.construct_tracks_to_dictionary(
            self.data, required_keys=required_keys
        )

    # plotting
    def overview_2d(
        self, x: str = "X", y: str = "Y", hue: str = "ID", **kwargs
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create a 2D overview plot of the data.

        Parameters:
        - x (str): The x-axis variable.
        - y (str): The y-axis variable.
        - hue (str): The hue variable.
        - **kwargs: Additional keyword arguments for the plot.

        Returns:
        - Union[plt.Figure, plt.Axes]: The figure or axes object.
        """

        return MFXDataAccessUtils.overview_2d(
            self.to_dataframe(), x=x, y=y, hue=hue, **kwargs
        )

    def show_track(
        self, ID: int, x: str = "X", y: str = "Y", hue: str = "T", **kwargs
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Show a specific track.

        Parameters:
        - track_dict (Dict[str, Dict[str, np.ndarray]]): The dictionary of tracks.
        - ID (int): The ID of the track to show.
        - x (str): The x-axis variable.
        - y (str): The y-axis variable.
        - hue (str): The hue variable.

        Returns:
        - Union[plt.Figure, plt.Axes]: The figure or axes object.
        """

        return MFXDataAccessUtils.show_track(
            self.track_dict, ID=ID, x=x, y=y, hue=hue, **kwargs
        )

    def plot_msd(
        self,
        ID: int
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Plot the mean squared displacement (MSD) over time.

        Parameters:
        - ID (int): The ID of the track to plot.
        - label (str): The label for the plot.
        - xlabel (str): The x-axis label.
        - ylabel (str): The y-axis label.

        Returns:
        - Union[plt.Figure, plt.Axes]: The figure or axes object.
        """
        if self.results is None:
            print("No results available.")
            return None
        
        if self.results.get("msd_container") is None:
            print("No MSD data available.")
            return None
        
        msd_container = self.get_msd_and_lags()

        return MFXDataAccessUtils.plot_msd(
            **msd_container[ID], title=f"Track {ID} Mean Squared Displacement",
            xlabel="Lags [s]",
            ylabel="MSD [nm²]"
        )

    def plot_msd_overview(self, **kwargs) -> Tuple[plt.Figure, plt.Axes]:
        """Plot the mean squared displacement (MSD) over time for all tracks.
        This function will plot the MSD for all tracks in the dataset.

        Args:
            label (str, optional): Plot title. Defaults to "MSD".
            xlabel (str, optional): Plot x label. Defaults to "Time [s]".
            ylabel (str, optional): Plot y label. Defaults to "MSD [nm²]".

        Returns:
            Union[plt.Figure, plt.Axes]: Returns the figure and axes objects.
        """

        if self.results is None:
            print("No results available.")
            return None
        
        if self.results.get("msd_container") is None:
            print("No MSD data available.")
            return None

        # get the MSD and lags
        msd_and_lags = self.get_msd_and_lags()

        return MFXDataAccessUtils.plot_msd_overview(
            msd_lags=msd_and_lags,
            title="Mean Squared Displacement Overview",
            xlabel="Lags [s]",
            ylabel="MSD [nm²]",
            **kwargs,
        )

    def plot_cycle_trace(
        self, ID: int, **kwargs
    ) -> Optional[Tuple[plt.Figure, plt.Axes]]:
        """Plots the cycle trace for a given ID. This will inform you on the MINFLUX tracking progression.

        Args:
            ID (int): Track ID to plot.
            **kwargs: Additional keyword arguments for the plot.

        Returns:
            Union[plt.Figure, plt.Axes]: Returns the figure and axes objects.
        """

        if self.results is None:
            print("No results available.")
            return None
        if self.results.get("cycle_container") is None:
            print("No cycle data available.")
            return None

        return MFXDataAccessUtils.plot_cycle_trace(
            integrated_cycles=np.diff(self.results["cycle_container"][ID]["INTEGRATED"]),
            dormant_cycles=np.diff(self.results["cycle_container"][ID]["DORMANT"]),
            upper_limit=int(
                self.metadata["cycle_stats_pre_split"]["TOT_median"]
                + self.metadata["cycle_stats_pre_split"]["TOT_std"]
                + 1
            ),
            title=f"Track {ID} Cycle Trace",
            **kwargs,
        )

    # show metadata
    def show_metadata(self) -> None:
        """
        Show the metadata of the dataset.
        """

        if self.metadata is not None:
            print("Metadata:")
            pprint(self.metadata)
        else:
            print("No metadata available.")

    def get_metadata(self) -> Optional[Dict]:
        """
        Get the metadata of the dataset.

        Returns:
        - Optional[Dict]: The metadata dictionary.
        """

        return self.metadata

    # results
    def condensed_motility_results(self) -> Dict:
        """
        Condense the results of the dataset.

        Returns:
        - Dict: The condensed results dictionary.
        """

        if self.results is not None:
            return {
                "unrestricted_time_average": self.results[
                    "unrestricted_time_fit_res"
                ].get("avr_time", None),
                "restricted_time_average": self.results["restricted_time_fit_res"].get(
                    "avr_time", None
                ),
                "unrestricted_ensemble_average": self.results[
                    "unrestricted_ensemble_fit_res"
                ].get("ensemble", None),
                "restricted_ensemble_average": self.results[
                    "restricted_ensemble_fit_res"
                ].get("ensemble", None),
            }
        else:
            print("No results available.")
            return {}

    def show_condensend_motility_results(self) -> None:
        """
        Show the results of the dataset.
        """

        if self.results is not None:
            print("Results:")
            pprint(self.condensed_motility_results())
        else:
            print("No results available.")

    def get_results(self) -> Optional[Dict]:
        """
        Get the results of the dataset.

        Returns:
        - Optional[Dict]: The results dictionary.
        """

        return self.results

    def get_condensed_motility_result_as_dataframe(self) -> pd.DataFrame:
        """
        Convert the condensed results to a pandas DataFrame.

        Returns:
        - pd.DataFrame: The results as a DataFrame.
        """

        if self.results is not None:
            return pd.DataFrame.from_dict(
                self.condensed_motility_results(), orient="index"
            )
        else:
            print("No results available.")
            return pd.DataFrame()

    def get_ergodicity(self) -> Optional[Dict]:
        """
        Get the ergodicity of the dataset.

        Returns:
        - Optional[Dict]: The ergodicity dictionary.
        """

        if self.results is not None:
            return {
                "unrestricted_ergodicity": self.results["unrestricted_ergodicity"].get(
                    "ergodicity", None
                ),
                "restricted_ergodicity": self.results["restricted_ergodicity"].get(
                    "ergodicity", None
                ),
            }
        else:
            print("No results available.")
            return None

    def get_msd(self) -> Optional[Dict]:
        """
        Get the mean squared displacement (MSD) of the dataset.

        Returns:
        - Optional[Dict]: The MSD dictionary.
        """
        # selectively return the MSD results
        if self.results is not None:
            if self.results.get("msd_container") is not None:
                return {
                    key: val.get("CYCLE_MSD", None)
                    for key, val in self.results["msd_container"].items()
                }
            else:
                print("No MSD results available.")
                return None

    def get_msd_errors(self) -> Optional[Dict]:
        """
        Get the errors of the mean squared displacement (MSD) of the dataset.

        Returns:
        - Optional[Dict]: The MSD errors dictionary.
        """
        # selectively return the MSD results
        if self.results is not None:
            if self.results.get("msd_container") is not None:
                return {
                    key: val.get("MSD_ERRORS", None)
                    for key, val in self.results["msd_container"].items()
                }
            else:
                print("No MSD results available.")
                return None

    def get_msd_and_lags(self) -> Optional[Dict]:
        """
        Get the mean squared displacement (MSD) and lags of the dataset.

        Returns:
        - Optional[Dict]: The MSD and timelines dictionary.
        """
        # selectively return the MSD results
        if self.results is not None:
            if self.results.get("msd_container") is not None:
                return {
                    key: {
                        "msd": val.get("CYCLE_MSD", None),
                        "lags": val.get("TIMELINE", None),
                    }
                    for key, val in self.results["msd_container"].items()
                }
            else:
                print("No MSD results available.")
                return None
            
    def get_cycle_info(self) -> Optional[Dict]:
        """
        Get the cycle information of the dataset.

        Returns:
        - Optional[Dict]: The cycle information dictionary.
        """

        if "cycle_container" in self.results:
            return self.results["cycle_container"]
        else:
            print("No cycle information available.")
            return None

    # exports
    def to_csv(self, file: str) -> None:
        """
        Save the data to a CSV file.

        Parameters:
        - file (str): The path to the output CSV file.
        """

        df = self.to_dataframe()
        df.to_csv(file, index=False)
