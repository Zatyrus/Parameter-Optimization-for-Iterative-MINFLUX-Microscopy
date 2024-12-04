## Dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

from typing import List, Dict, Any, Union
from numpy.lib.npyio import NpzFile

class MFXDataAccessUtils:
    ## Functions
    @staticmethod
    def grab_file_paths(root:str, filetype:str = '.npz')->List:
        '''
        Function to grab all file paths in a directory.
        '''
        return glob(f"{root}/**/*{filetype}", recursive=True)

    @staticmethod
    def load_npz(file:str, print_keys:bool = False)->Dict:
        '''
        Function to load a .npz file. Will display the keys set in the file.
        '''
        out = np.load(file)
        if print_keys:
            print(f"Keys in file: {out.files}")
        return out
    
    @staticmethod
    def load_as_matrix(file:str)->np.ndarray:
        '''
        Function to load a .npz file as a matrix.
        '''
        out = np.load(file)
        return np.stack([out[key] for key in out.files], axis=1)

    @staticmethod
    def load_npz_as_df(file:str)->pd.DataFrame:
        '''
        Function to load a .npz file as a pandas DataFrame.
        '''
        out = np.load(file)
        return pd.DataFrame({key: out[key] for key in out.files})

    # For further use
    @staticmethod
    def load_npz_as_dict(file:str)->Dict:
        '''
        Function to load a .npz file as a dictionary.
        '''
        out = np.load(file)
        return {key: out[key] for key in out.files}

    @staticmethod
    def load_npz_with_specific_keys(file:str, keys:List[str])->Dict:
        '''
        Function to load a .npz file with specific keys.
        '''
        out = np.load(file)
        return {key: out[key] for key in keys}

    @staticmethod
    def load_as_matrix(file:str)->np.ndarray:
        '''
        Function to load a .npz file as a matrix.
        '''
        out = np.load(file)
        return np.stack([out[key] for key in out.files], axis=1)

    @staticmethod
    def cast_to_matrix(file:NpzFile, ignore_keys:List[str] = ['ID'])->np.ndarray:
        '''
        Function to cast a .npz file to a matrix.
        '''
        return np.stack([file[key] for key in file.files if key not in ignore_keys], axis=1), [key for key in file.files if key not in ignore_keys]

    @staticmethod
    def construct_tracks_to_matrices(file:str)->Dict[str, np.ndarray]:
        '''
        Function to extract tracks from a .npz file and return them as a dictionary of matrices.
        '''
        
        out = MFXDataAccessUtils.load_npz(file)
        
        # Extract the unique IDs. we need these to construct the tracks
        ID_arr = out.get("ID")
        un = np.unique(ID_arr).astype('uint16')

        out, _ = MFXDataAccessUtils.cast_to_matrix(file = out,
                                                   ignore_keys = ['ID'])

        return {ID: out[np.argwhere(ID_arr == ID).flatten(),:] for ID in un}

    @staticmethod
    def construct_tracks_to_dictionary(file:str, required_keys:List[str])->Dict[str, Dict[str, np.ndarray]]:
        
        out = MFXDataAccessUtils.load_npz(file)
        
        # Extract the unique IDs. we need these to construct the tracks
        ID_arr = out.get("ID")
        un = np.unique(ID_arr).astype('uint16')

        out, keys = MFXDataAccessUtils.cast_to_matrix(file = out,
                                                      ignore_keys = ['ID'])

        data_dict = {ID: out[np.argwhere(ID_arr == ID).flatten(),:] for ID in un}
        return {ID: {key: data_dict[ID][:,i] for i, key in enumerate(keys) if key in required_keys} for ID in un}

    ## Plotting
    @staticmethod
    def overview_2d(data:pd.DataFrame, x:str, y:str, hue:str)->Union[plt.Figure, plt.Axes]:
        '''
        Function to plot a 2D overview of the data.
        '''
        
        fig, ax = plt.subplots(figsize=(6, 5), dpi = 100)
        img = ax.scatter(x = data[x], 
                         y = data[y], 
                         c = data[hue], 
                         alpha = 0.5,
                         s = 3,
                         cmap='magma',
                         label = f"color: {hue}")
        
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(f"{x} vs {y}")
        fig.colorbar(mappable = img)
        
        fig.tight_layout()
        
        return fig, ax
    
    @staticmethod
    def show_track(track_dict:Dict[str, Dict[str, np.ndarray]], ID:int, x:str, y:str, hue:str)->Union[plt.Figure, plt.Axes]:
        '''
        Function to plot a track.
        '''
        fig, ax = plt.subplots(figsize=(6, 5), dpi = 100)
        # plot connection lines
        ax.plot(track_dict[ID][x], 
                track_dict[ID][y], 
                color = 'black', 
                alpha = 0.5, 
                lw = 1,
                zorder=1)
        img = ax.scatter(x = track_dict[ID][x],
                         y = track_dict[ID][y], 
                         c = track_dict[ID][hue],
                         s = 15,
                         cmap = 'magma',
                         label = f"color: {hue}",
                         zorder=2)
        
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(f"Track {ID}")
        ax.legend()
        fig.colorbar(mappable = img)
        
        fig.tight_layout()
        
        return fig, ax