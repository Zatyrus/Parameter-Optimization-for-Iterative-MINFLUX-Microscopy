# About
This repository contains the data made available for the paper "Parameter Optimization for Iterative MINFLUX Microscopy" currently under review at Communications Biology. We also provide a small selection of code to read, format and export the data for your own use.

The data made available here is an excerpt of the original files that is formatted for ease of use. The `raw` sets have been extracted from the propriatory MINFLUX files produced by the MINFLUX-IMSPECTOR software (Abberior GmbH). The values are provided **unaltered**. 

The sets used in the analysis part of our paper, were **processed** as stated in [Data Processing](#data-processing).

# Data Access Utils
We provide a small set of utilities to access the data in the `.npz` files. These can be accessed under `data_access_tools/data_tools.py` and `data_access_tools/dataset`. Please, find a demo of the access tools under `data_access_tools/how_to_access_the_data.ipnyb`.

Feel free to use the methods found here in your own code.

## Python Environment
Requirements: [miniconda](https://docs.conda.io/en/latest/miniconda.html) or [anaconda](https://www.anaconda.com/products/distribution) installed.
Dont forget that you can "**skip registration**" even when installing anaconda don't get confused by the [dark pattern](https://en.wikipedia.org/wiki/Dark_pattern) they put up. 

### Create the environment
Open a terminal or anaconda prompt and navigate to the root of the repository. Then run the following command:
```bash
conda env create -f python_env.yml
```
After that you can activate the environment with:
```bash
conda activate MFX_data
```

# Directory Structure - Where to find what
```bash
root:.
├───.ruff_cache
│   └───0.11.8
├───data
│   ├───npz_files_processed
│   │   ├───change_DMP
│   │   ├───change_dT
│   │   ├───change_PL
│   │   ├───dye_sample
│   │   └───TIRF_Reference
│   └───npz_files_raw
│       ├───change_DMP
│       ├───change_dT
│       ├───change_PL
│       ├───dye_sample
│       └───TIRF_reference
├───data_access_utils
│   └───__pycache__
├───sequences
│   ├───container
│   └───custom
│       ├───background
│       ├───change_DMP
│       ├───change_DT
│       ├───change_PL
│       └───dye_sample
└───sequence_utils
    └───__pycache__
```
### Data Directory
The data is stored in the `data` directory. The data is split into two directories: `npz_files_raw` and `npz_files_processed`. The `raw` files contain the original data as extracted from the files exported from the MINFLUX-*iMSPECTOR* software. The `processed` files are the files that have been filtered and analyzed as described in [Data Processing](#data-processing).

We chose the `.npz` format to store the files in a conveneint and efficient way. The data is stored in a dictionary with the following keys:
```python
['Z', 'Y', 'X', 'T', 'ECO', 'EFO', 'TID', 'TIC', 'ITR', 'ID']
```
### Sequence Directory
The sequence files are stored in the `sequences` directory and split into two directories: `container` and `custom`. The `container` directory contains default sequence iteraion blocks provided by the manufacturer (Abberior Instruments GmbH). These sequence files can be used to generate and or modify the MINFLUX sequences for the experiments. 

The `custom` directory contains the custom sequence files used for our experiments. The sequence files are stored in a directory structure that reflects the experiment they were used in.

All `custom` files are stored in the `.json` format and can be implemented straight forwardly into your own experiments. They can be opened and modified with any text editor. We advise to consult Appendix II - Parameter Overview of the journal article.

### Data Access Utils
The data access utils are stored in the `data_access_utils` directory. The directory contains two files: `data_tools.py` and `dataset.py`. The `data_tools.py` file contains the functions to access the data in the `.npz` files. The `dataset.py` file contains the class to access the data in the `.npz` files. The class is used to store the data and metadata in a convenient way. A demo of the access tools can be found in the `data_access_utils/how_to_access_the_data.ipynb` file. The demo shows how to use the data access tools to access the data in the `.npz` files. The demo is a Jupyter notebook and can be opened with any Jupyter notebook viewer.

### Sequence Utils
We provide a small set of verification tools to quickly check for sequence duplications or id-filename-mismatches that can occur when modifying the sequence files and lead to unexpected errors during the experiment.

Use the script found in `sequence_utils/verify_sequences.py` either from CLI or via Python. Please, find a demo of the sequence verification tool under ``sequence_utils/how_to_verify_the_sequences.ipynb``. The demo shows how to use the sequence verification tool to check for sequence duplications or id-filename-mismatches. The demo is a Jupyter notebook and can be opened with any Jupyter notebook viewer.

## Data Format
The data is stored in the `.npz` format. The raw data is stored in a dictionary with the following keys:
```python
['Z', 'Y', 'X', 'T', 'ECO', 'EFO', 'TID', 'TIC', 'ITR', 'ID']
```
The processed data is stored in the same format, but with additional metadata and results that contain the extracted information of the particle motility. Both are stored as dictionaries and can be access with the `dataset` class found in `data_access_tools/dataset.py`. The results are indicated witht he following keys:
```python
[
  'unrestricted_ensemble_fit_res',
  'restricted_ensemble_fit_res',
  'unrestricted_time_fit_res', 
  'restricted_time_fit_res', 
  'unrestricted_ergodicity', 
  'restricted_ergodicity'
]
```
Where the `unrestricted` and `restricted` refer to the two different ways to access the MSD regimes: The `Lower MSD Regime`, i.e. `unrestricted` and the `Upper MSD Regime`, i.e. `restricted`. The `ensemble` and `time` refer to the two different methods used to fit the data. The `unrestricted_ensemble_fit_res` contains the results of the unrestricted ensemble fit, while the `restricted_ensemble_fit_res` contains the results of the restricted ensemble fit. The same applies for the time fits. Additionally, the time fit resilts contain the diffusion coefficient extracted for each trajectory and the average diffusion coefficient for the entire dataset. The `unrestricted_ergodicity` and `restricted_ergodicity` contain the ergodicity of the data, i.e. the ratio of the ensemble average to the time average.
The ergodicity is calculated as follows:
$$\text{ergodicity}=\frac{\langle MSD \rangle_{ensemble}}{\langle MSD \rangle_{time}}$$

Where $\langle MSD \rangle_{ensemble}$ is the ensemble average of the MSD and $\langle MSD \rangle_{time}$ is the time average of the MSD. The ergodicity is a measure of how well the data fits the ergodic hypothesis, i.e. how well the ensemble average and time average agree with each other. An isotropic process is expected to have an ergodicity of 1, while a non-ergodic process is expected to have an ergodicity of less than 1. 

## Data Processing
The data was processed in the following way:
1. Discard all traces with less than 50 and more than 1500 localizations.
2. Set starting time to 0 for all traces.
3. Set the range of IDs to [0, N-1] with N being the number of traces.
4. Filter for immobilized particles using ['blob-be-gone'](https://www.frontiersin.org/articles/10.3389/fbinf.2023.1268899/full) algorithm. We used the following weights: 
```python
    {
        'MAX_DIST':1,
        'CV_AREA':1,
        'SPHE':2, 
        'ELLI':1,
        'CV_DENSITY':2,
    }
```
We did not filter for immobilized particles the lipid-deposition [*FLOW*] data, as there were very little particles that were immobilized and the filtering process would've been damaging to the data.
5. Remove Jump and Jitter artifacts.
   1. Extract MINFLUX time signal from data.
   2. Cut traces whenever jump or jitter artifacts are detected.
   3. Remove traces with less than 50 localizations.
6. Filter for immobilized particles using ['blob-be-gone'](https://www.frontiersin.org/articles/10.3389/fbinf.2023.1268899/full) algorithm. We used the following weights: 
```python
    {                                
        'MAX_DIST':1,
        'CV_AREA':1,
        'SPHE':2, 
        'ELLI':1, 
        'CV_DENSITY':2
    }
```
We did not filter for immobilized particles the lipid-deposition [*FLOW*] data, as there were very little particles that were immobilized and the filtering process would've been damaging to the data.

7. Calculate the Mean Squared Displacement (MSD), i.e. a custom implementation of the [MSD](https://en.wikipedia.org/wiki/Mean_squared_displacement) algorithm to suit inhomogeneous lag-times encountered in the MINFLUX data. 
8. Calculate the Optimized Least Squares Fit (OLSF) of the MSD data to extract the diffusion coefficient. The OLSF is a custom implementation of the algorithm described by Michalet et al. in [Optimal diffusion coefficient estimation in single-particle tracking](https://doi.org/10.1103/PhysRevE.85.061916) to suit the inhomogeneous lag-times encountered in the MINFLUX data.

All information gathered during the processign steps is stored in the `metadata` dictionary of the `npz` files. The metadata is stored in a dictionary.


## Data Field Description
#### ``X,Y,Z``
- **value**: Any ``float``.
- **content**: The x, y, z coordinates of the emitter in the 3D space. The coordinates are given in nanometers. As our experiments are 2D, the z-coordinate is always 0.

#### ``T``
- **value**: Any positive ``float``.
- **content**: States the time in seconds of sucessful position estimation relative to the point in time the measurement has been started. 

#### ``ECO``
- **value**: Any positive ``integer``.
- **content**: The ``effective-count-(at)-offset (eco)`` states the sum of photons collected during all TCP cycles.

#### ``EFO``
- **value**: Any positive ``float``.
- **content**: The ``effective-frequency-(at)-offset (efo)`` states the total emission frequency of photons collected during all TCP cycles. It is calculated as follows: 
  $$\text{EFO}=\frac{\text{ECO}}{\eta \cdot t_{dwell}}$$
  With $\eta$ being the number of integrated TCP cycles.

#### ``TID``
- **value**: Any positive ``integer``.
- **content**: The ``track/trace-id (tid)`` is given to each sucessfully concluded photon burst trace. Localizations with the same ``tid`` are recorded for the "same" photon burst event. This alone is however **NOT** a valid measure to separate single particles, as they can be recorded in continuation under one single ``tid``
  
#### ``ITR``
- **value**: Any positive ``integer`` $\in[0,\text{num}_{iterations}-1]$
- **content**: Iteration ID; Only the last one will retrun a localization.

#### ``TIC``
- **value**: Any positive ``integer``.
- **content**: Internal clock tic of the used FPGA.

# Acquisition Parameters
**Experimental MINFLUX Scanning Parameters for 2D Single Particle Tracking of Fluorescent QDot-labeled Lipid Analogues in the SLB** – **(*)** marks the parameters that were changed for the experiments.
| **2D Tracking**                 | Pinhole Orbit [I] | 1st MFX Iteration [II] | 2nd MFX Iteration [III]  |
|:-------------------------------:|:-----------------:|:----------------------:|:------------------------:|
| **L (nm)**                      | 284               | 302                    | 150                      |
| **Pattern Shape**               | Hexagon           | Hexagon                | Hexagon                  |
| **Photon Limit (counts)**       | 40                | 20                     | 50 (*)                   |
| **Laser Power Factor (times)**  | 1                 | 1.5                    | 2.0 (*)                  |
| **Pattern dwell time (µs)**     | 500               | 100                    | 200 (*)                  |
| **Pattern repeat (times)**      | 1                 | 1                      | 1                        |
| **CFR Threshold**               | -1                | 0.5                    | -1                       |
| **Background Threshold (kHz)**  | 15                | 30                     | 30 (*)                   |
| **MaxOffTime (control param.)** | 3ms               | 3ms                    | 3ms                      |
| **Damping (control param.)**    | 0                 | 0                      | 0                        |
| **Headstart (control param.)**  | -1                | -1                     | -1                       |
| **Stickiness (control param.)** | 4                 | 4                      | 4                        |

# Extended Data Availability
Should you require the full data set as exported from the MINFLUX-IMSPECTOR and/or sequence file, please contact the corresponding author. The data is stored in a proprietary format and can be made available upon request.