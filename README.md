# About
This repository contains the data made available for the paper "Parameter Optimization for Iterative MINFLUX Microscopy" currently under review at Communications Biology. We also provide a small selection of code to read, format and export the data for your own use.

The data made available here is an excerpt of the original files that is formatted for ease of use. The `raw` set have been extracted from the propriatory MINFLUX `.npy`-files produced by the Abberior (GmbH) MINFLUX-IMSPECTOR. They are provided **unaltered**. 

The `filtered` sets were **processed** as stated in [Data Processing](#data-processing).

# Data
The data is can be found in the following directory strcuture under `data`:
```bash
root:.
├───data
│   ├───change_dwell_time
│   │   ├───filtered
│   │   └───raw
│   └───change_photon_limit
│       ├───filtered
│       └───raw
└───data_access_utils

```

We chose the `.npz` format to store the files in a conveneint and efficient way. The data is stored in a dictionary with the following keys:
```python
['Z', 'Y', 'X', 'T', 'ECO', 'EFO', 'TID', 'TIC', 'ITR', 'ID']
```
## Data Processing
The data was processed in the following way:
1. Discard all traces with less than 50 localizations.
2. Set starting time to 0 for all traces.
3. Set the range of IDs to [0, N-1] with N being the number of traces.
4. Remove Jump and Jitter artifacts.
   1. Extract MINFLUX time signal from data.
   2. Cut traces whenever jump or jitter artifacts are detected.
   3. Remove traces with less than 50 localizations.
5. Remove blob-artifacts using [blob-b-gone](https://www.frontiersin.org/journals/bioinformatics/articles/10.3389/fbinf.2023.1268899/full).

### Nomenclature
We use the following nomenclature for the files:
```bash
<experiment>_<set_type>_<tolerated_noise_limit>-<jitter_limit>-<jump_limit>_<blob-b-gone_used>.npz
```
Where:
- `<experiment>`: The experiment the data was taken from.
- `<set_type>`: The type of set the data belongs to. [raw, processed]
- `<tolerated_noise_limit>`: Lower threshold for cycle counts seen as toleratable noise; set to $\textsf{median}(\eta)$. Anything below that is treated as trivial noise.
- `<jitter_limit>`: Lower threshold for cycle counts seen as jitter; set to $\textsf{median}(\eta)+1\sigma$. 
- `<jump_limit>`: Lower threshold for cycle counts seen as jumps; set to $\textsf{median}(\eta)+2\sigma$. 
- `<blob-b-gone_used>`: Whether the blob-b-gone (BBEG) algorithm was used to remove blob artifacts. [BBEG, noBBEG]


# Data Access Utils
We provide a small set of utilities to access the data in the `.npz` files. The utilities are stored in `data_access_tools/tools.py`. We showcase the usage of the utilities in the following code in the `data_access_tools/how_to_get_your_data.ipnyb`.

Feel free to use the utilities in your own code.

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

# Data Field Description
## Position and Time
#### ``X,Y,Z``
- **value**: Any ``float``.
- **content**: The x, y, z coordinates of the emitter in the 3D space. The coordinates are given in nanometers. As our experiments are 2D, the z-coordinate is always 0.

#### ``T``
- **value**: Any positive ``float``.
- **content**: States the time in seconds of sucessful position estimation relative to the point in time the measurement has been started. 

## Photon Information
#### ``ECO``
- **value**: Any positive ``integer``.
- **content**: The ``effective-count-(at)-offset (eco)`` states the sum of photons collected during all TCP cycles.

#### ``EFO``
- **value**: Any positive ``float``.
- **content**: The ``effective-frequency-(at)-offset (efo)`` states the total emission frequency of photons collected during all TCP cycles. It is calculated as follows: 
  $$\text{EFO}=\frac{\text{ECO}}{k \cdot t_{dwell}}$$
  With $k$ being the number of integrated TCP cycles.

## Iteration and Trace Information (optional)
#### ``TID``
- **value**: Any positive ``integer``.
- **content**: The ``track/trace-id (tid)`` is given to each sucessfully concluded photon burst trace. Localizations with the same ``tid`` are recorded for the "same" photon burst event. This alone is however **NOT** a valid measure to separate single particles, as they can be recorded in continuation under one single ``tid``
  
#### ``ITR``
- **value**: Any positive ``integer`` $\in[0,\text{num}_{iterations}-1]$
- **content**: Iteration ID; Only the last one will retrun a localization.

## Technical Information (optional)
#### ``TIC``
- **value**: Any positive ``integer``.
- **content**: Internal clock tic of the used FPGA.

# Extended Data Availability
Should you require the full data set as exported from the MINFLUX-IMSPECTOR and/or sequence file, please contact the corresponding author. The data is stored in a proprietary format and can be made available upon request.