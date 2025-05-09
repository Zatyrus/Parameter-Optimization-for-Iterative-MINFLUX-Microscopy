## Dependencies
import numpy as np
import pandas as pd

from pprint import pprint
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional, Union
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
    ) -> Union[plt.Figure, plt.Axes]:
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
    ) -> Union[plt.Figure, plt.Axes]:
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
    def condensed_results(self) -> Dict:
        """
        Condense the results of the dataset.

        Returns:
        - Dict: The condensed results dictionary.
        """

        if self.results is not None:
            return {'unrestricted_time_average': self.results['unrestricted_time_fit_res'].get('avr_time', None),
                    'restricted_time_average': self.results['restricted_time_fit_res'].get('avr_time', None),
                    'unrestricted_ensemble_average': self.results['unrestricted_ensemble_fit_res'].get('ensemble', None),
                    'restricted_ensemble_average': self.results['restricted_ensemble_fit_res'].get('ensemble', None)}
        else:
            print("No results available.")
            return {}
    
    def show_condensend_results(self) -> None:
        """
        Show the results of the dataset.
        """

        if self.results is not None:
            print("Results:")
            pprint(self.condensed_results())
        else:
            print("No results available.")
    
    def get_results(self) -> Optional[Dict]:
        """
        Get the results of the dataset.

        Returns:
        - Optional[Dict]: The results dictionary.
        """

        return self.results
    
    def get_condensed_result_as_dataframe(self) -> pd.DataFrame:
        """
        Convert the condensed results to a pandas DataFrame.

        Returns:
        - pd.DataFrame: The results as a DataFrame.
        """

        if self.results is not None:
            return pd.DataFrame.from_dict(self.condensed_results(), orient="index")
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
                'unrestricted_ergodicity': self.results['unrestricted_ergodicity'].get('ergodicity', None),
                'restricted_ergodicity': self.results['restricted_ergodicity'].get('ergodicity', None),
            }
        else:
            print("No results available.")
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
