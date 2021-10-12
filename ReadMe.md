# HDF

## Description

- Current version: 5
- Binary file format
- Usual extensions: `.hdf5` or `.h5`
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

| Format              | Size (MB) |
| ------------------- | --------: |
| Log Data            | 41.929378 |
| CSV                 | 13.388231 |
| HDF5 Zfp            |  6.262768 |
| HDF5 FciDecomp      |  6.262760 |
| HDF5 No Compression |  6.250103 |
| HDF5 LZF            |  3.360693 |
| HDF5 LZ4            |  2.998656 |
| HDF5 Blosc          |  1.913076 |
| HDF5 GZip           |  1.731552 |
| HDF5 Bitshuffle     |  1.709330 |
| HDF5 Zstd           |  1.388591 |

### Tool

For the data above we used the Python script [`convert.py`](Source/convert.py):

```sh
python Source/convert.py
```

The script will store the output files in the directory [`Data`](Data). Afterward we used the **Unix** command:

```sh
ls -lS Data/*
```

to print the size of the converted files.

#### Requirements

To use the script you need Python `3.9` or later and the

- [`h5py`](https://www.h5py.org) and
- [`hdf5plugin`](https://pypi.org/project/hdf5plugin/)

packages:

```sh
pip install h5py hdf5plugin
```
