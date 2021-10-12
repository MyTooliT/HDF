# -- Imports ------------------------------------------------------------------

from csv import DictWriter
from pathlib import Path
from re import compile

from h5py import File
from hdf5plugin import Bitshuffle, Blosc, FciDecomp, LZ4, Zfp, Zstd
from numpy import asarray, recarray, uint8, uint16, uint64
from tables import (Filters, IsDescription, open_file, UInt8Col, UInt16Col,
                    UInt64Col)

# -- Classes ------------------------------------------------------------------


class Converter:
    """Convert acceleration log data to other formats"""
    def __init__(self, filepath):
        """Initialize the log object using the log data of the given file

        Parameters
        ----------

        filepath:
            The filepath of a log file that stores acceleration data

        """

        self.filepath = Path(filepath)

        # Store log data in line based format
        self.values = None
        self._read_log()

        # Store log data in row based format
        self.counters = []
        self.timestamps = []
        self.acceleration = []
        self._store_rows()

    def _read_log(self):
        """Read acceleration log data"""

        line_regex = compile(r"\[I\]\s*\(\d+ms\)[^\d]+(?P<counter>\d+)"
                             r"[^\d]+(?P<timestamp>\d+(\.\d+)?)[^\d]+"
                             r"(?P<acceleration>\d+);")
        values = []
        with open(self.filepath) as file:
            for line in file:
                match = line_regex.match(line)
                if match:
                    values.append({
                        'counter':
                        int(match['counter']),
                        'timestamp':
                        int(float(match['timestamp']) * 1000),
                        'acceleration':
                        int(match['acceleration'])
                    })

        self.values = values

    def _store_rows(self):
        """Store acceleration data as rows"""

        for value in self.values:
            self.counters.append(value['counter'])
            self.timestamps.append(value['timestamp'])
            self.acceleration.append(value['acceleration'])

    def store_csv(self):
        """Store acceleration data in CSV file"""

        with open(self.filepath.with_suffix(".csv"), 'w',
                  newline='') as csvfile:
            fieldnames = ['counter', 'timestamp', 'acceleration']
            writer = DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(self.values)

    def store_hdf_h5py(self, compression_name, **compression_options):
        """Store acceleration data in HDF5 file using h5py

        Parameters
        ----------

        compression_name:
            A human readable name of the compression filter

        compression_options:
            A dictionary like object that specifies compression options

        """

        types = [('counter', uint8), ('timestamp', uint64),
                 ('acceleration', uint16)]
        number_lines = len(self.values)
        data = recarray(number_lines, dtype=types)
        data['counter'] = asarray(self.counters)
        data['timestamp'] = asarray(self.timestamps)
        data['acceleration'] = asarray(self.acceleration)

        filepath = self.filepath.with_name(
            f"{self.filepath.stem} h5py {compression_name}").with_suffix(
                ".hdf5")
        with File(filepath, 'w') as hdf:
            hdf.create_dataset("acceleration",
                               data=data,
                               shape=(number_lines, ),
                               **compression_options)

    def store_hdf_pytables(self, filters=None):
        """Store acceleration data in HDF5 file using h5py

        Parameters
        ----------

        filters:
            The filter that should be used to store the file

        """
        class Acceleration(IsDescription):
            counter = UInt8Col()
            timestamp = UInt64Col()
            acceleration = UInt16Col()

        compression_name = ("No Compression"
                            if filters is None else filters.complib)
        filepath = self.filepath.with_name(
            f"{self.filepath.stem} PyTables {compression_name}").with_suffix(
                ".hdf5")
        with open_file(filepath, 'w', filters=filters) as hdf:
            data = hdf.create_table(hdf.root, "acceleration", Acceleration)
            row = data.row
            for value in self.values:
                row['counter'] = value['counter']
                row['timestamp'] = value['timestamp']
                row['acceleration'] = value['acceleration']
                row.append()


# -- Main ---------------------------------------------------------------------

if __name__ == '__main__':
    print("Read log data")

    # =======
    # = CSV =
    # =======

    converter = Converter("Data/Log.txt")
    print("Store CSV file")
    converter.store_csv()

    # ========
    # = h5py =
    # ========

    compression_options = [{
        'compression': None,
        'compression_name': "No Compression"
    }, {
        'compression': "gzip",
        'compression_name': "GZip"
    }, {
        'compression': "lzf",
        'compression_name': "LZF"
    }]
    compression_algorithms = [
        Bitshuffle(),
        Blosc(),
        FciDecomp(),
        LZ4(),
        Zfp(),
        Zstd(),
    ]
    compression_options.extend([{
        'compression_name': type(compression).__name__,
        **compression
    } for compression in compression_algorithms])

    for compression_option in compression_options:
        name = compression_option['compression_name']
        name = name.lower() if name == "No Compression" else name
        print(f"Store h5py data using {name} algorithm")
        converter.store_hdf_h5py(**compression_option)

    # ============
    # = PyTables =
    # ============

    filters_list = [
        None,
        Filters(4, 'zlib'),
        Filters(4, 'lzo'),
        Filters(4, 'blosc'),
    ]
    for filters in filters_list:
        name = "no compression" if filters is None else filters.complib
        print(f"Store PyTables data using {name} algorithm")
        converter.store_hdf_pytables(filters)
