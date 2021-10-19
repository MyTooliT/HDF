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

- [PyTables](http://www.pytables.org)

  - Database like interface to HDF5
  - Installation requires HDF5 C library or binary wheel file ([Windows](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pytables))

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

| Format                  | Size (MB) | Works in HDFView |
| ----------------------- | --------: | :--------------: |
| Log Data                | 41.929378 |                  |
| CSV                     | 13.388231 |                  |
| PyTables No Compression |  6.299136 |        ✅        |
| h5py Zfp                |  6.262768 |        ✅        |
| h5py FciDecomp          |  6.262760 |        ✅        |
| h5py No Compression     |  6.250103 |        ✅        |
| h5py LZF                |  3.360693 |        ❌        |
| h5py LZ4                |  2.998656 |        ❌        |
| h5py Blosc              |  1.913076 |        ❌        |
| h5py GZip               |  1.731552 |        ✅        |
| h5py Bitshuffle         |  1.709330 |        ❌        |
| PyTables lzo            |  1.630033 |        ❌        |
| PyTables blosc          |  1.540903 |        ❌        |
| h5py Zstd               |  1.388591 |        ❌        |
| PyTables zlib           |  1.137004 |        ✅        |

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

- [`h5py`](https://www.h5py.org),
- [`tables`](http://www.pytables.org), and
- [`hdf5plugin`](https://pypi.org/project/hdf5plugin/)

packages:

```sh
pip install h5py hdf5plugin tables
```
