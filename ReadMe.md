# HDF

## Description

- Current version: 5
- Binary file format
- Usual extension: `.hdf5`
- **Groups**:
  - Specify location of data
  - Can be compared to directory/dictionary keys
- **Data Sets**:
  - Store data
  - Can be compared to multidimensional arrays/tables

## Information

- [Learning HDF5](https://portal.hdfgroup.org/display/HDF5/Learning+HDF5)

## Libraries

- [h5py](http://h5py.org)

  - Mapping from HDF5 library to Python and `numpy`
  - Seems to be a [little slower than PyTables](https://stackoverflow.com/questions/57953554)
  - **Size of data is fixed** and can be resized later up to a fixed chosen maximum
    - This should not be a big problem since storing a large amount of data with value `0` still results in a `1` KB file
  - [Example](Source/h5.py)

- [PyTables](http://www.pytables.org)
  - Database like interface to HDF5
  - Installation requires HDF5 C library
  - [Example](Source/pytables.py)

## Tools

- [`h5dump`](https://portal.hdfgroup.org/display/support/Downloads)
  - Prints data contained in an HDF5 file
  - Contained in `HDF5` software distribution ([macOS](https://formulae.brew.sh/formula/hdf5))
- [ViTables](https://vitables.org)
  - Graphical viewer and editor for HDF5 files
- [HDF View](https://www.hdfgroup.org/downloads/hdfview/)
  - Official graphical viewer and editor for HDF files

## Comparison

Data sizes for 60 seconds of measurement data containing:

- time in ms since file creation
- message counter
- time stamp
- acceleration value

| Log File | CSV     | HDF (Uncompressed) |
| -------- | ------- | ------------------ |
| ~ 42 MB  | ~ 17 MB | ~ 18 MB            |

### Tool

For the data above we used the Python script [`convert.py`](Source/convert.py):

```sh
python Source/convert.py
```

The script will store the output files in the directory [`Data`](Data).

#### Requirements

To use the script you need Python `3.9` or later and the [`h5py`](https://www.h5py.org) package:

```sh
pip install h5py
```
