# -- Imports ------------------------------------------------------------------

from os import unlink

from h5py import File

# -- Function -----------------------------------------------------------------


def create_hdf(filename):
    with File("h5py.hdf5", 'w') as test:
        print(
            "Create two dimensional data set “simple” with integer data type")
        data = test.create_dataset("simple", (100, ), dtype='i')
        print("Set first element to 1337")
        data[0] = 1337
        data = test['simple']  # You can also access data using keys
        print("Set third element to 42")
        data[2] = 42
        print("Print first five elements of data set “simple”")
        print(data[0:5])


# -- Main ---------------------------------------------------------------------

if __name__ == '__main__':
    filename = "h5py.hdf5"
    create_hdf(filename)
    unlink(filename)
