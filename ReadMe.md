# HDF

## Description

- Current version 5
- Binary file format
- **Groups**:
  - Specify location of data
  - Can be compared to directory/dictionary keys
- **Data Sets**:
  - Store data
  - Can be compared to multidimensional arrays/tables

## Links

### Information

- [Learning HDF5](https://portal.hdfgroup.org/display/HDF5/Learning+HDF5)

### Libraries

- [h5py](http://h5py.org)

  - Mapping from HDF5 library to Python and `numpy`
  - Seems to be a [little slower than PyTables](https://stackoverflow.com/questions/57953554)

- [PyTables](http://www.pytables.org)
  - Database like interface to HDF5

### Tools

- [`h5dump`](https://portal.hdfgroup.org/display/support/Downloads)
  - Prints data contained in an HDF5 file
  - Contained in `HDF5` software distribution ([macOS](https://formulae.brew.sh/formula/hdf5))
- [ViTables](https://vitables.org)
  - Graphical viewer and editor for HDF5 files
- [HDF View](https://www.hdfgroup.org/downloads/hdfview/)
  - Official graphical viewer and editor for HDF files
