# -- Imports ------------------------------------------------------------------

from os import unlink

from tables import Int32Col, IsDescription, open_file

# -- Class --------------------------------------------------------------------


class Simple(IsDescription):
    value = Int32Col()


# -- Function -----------------------------------------------------------------


def create_hdf(filename):
    with open_file(filename, 'w') as test:
        root = test.root
        print("Create table “simple” with integer data type")
        data = test.create_table(root, "simple", Simple)
        row = data.row
        print("Set first element to 1337")
        row['value'] = 1337
        row.append()
        row['value'] = 0
        row.append()
        print("Set third element to 42")
        row['value'] = 42
        row.append()


# -- Main ---------------------------------------------------------------------

if __name__ == '__main__':
    filename = "tables.hdf5"
    create_hdf(filename)
    unlink(filename)
