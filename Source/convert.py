# -- Imports ------------------------------------------------------------------

from csv import DictWriter
from pathlib import Path
from re import compile

from h5py import File
from numpy import asarray, recarray

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
        self.milliseconds = []
        self.counters = []
        self.timestamps = []
        self.acceleration = []
        self._store_rows()

    def _read_log(self):
        """Read acceleration log data"""

        line_regex = compile(r"\[I\]\s*\((?P<ms>\d+)ms\)[^\d]+(?P<counter>\d+)"
                             r"[^\d]+(?P<timestamp>\d+(\.\d+)?)[^\d]+"
                             r"(?P<acceleration>\d+);")
        values = []
        with open(self.filepath) as file:
            for line in file:
                match = line_regex.match(line)
                if match:
                    values.append({
                        'millisecond': match['ms'],
                        'counter': match['counter'],
                        'timestamp': match['timestamp'],
                        'acceleration': match['acceleration']
                    })

        self.values = values

    def _store_rows(self):
        """Store acceleration data as rows"""

        for value in self.values:
            self.milliseconds.append(value['millisecond'])
            self.counters.append(value['counter'])
            self.timestamps.append(value['timestamp'])
            self.acceleration.append(value['acceleration'])

    def store_csv(self):
        """Store acceleration data in CSV file"""

        with open(self.filepath.with_suffix(".csv"), 'w',
                  newline='') as csvfile:
            fieldnames = [
                'millisecond', 'counter', 'timestamp', 'acceleration'
            ]
            writer = DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(self.values)

    def store_hdf(self, compression=None):
        """Store acceleration data in HDF5 file

        Parameters
        ----------

        compression:
            The algorithm that should be used to compress the data

        """

        types = [('millisecond', int), ('counter', int), ('timestamp', float),
                 ('acceleration', int)]
        number_lines = len(self.milliseconds)
        data = recarray(number_lines, dtype=types)
        data['millisecond'] = asarray(self.milliseconds)
        data['counter'] = asarray(self.counters)
        data['timestamp'] = asarray(self.timestamps)
        data['acceleration'] = asarray(self.acceleration)

        algorithm = ("No" if compression is None else compression.capitalize())
        filepath = self.filepath.with_name(
            f"{self.filepath.stem}{algorithm}Compression").with_suffix(".hdf5")
        with File(filepath, 'w') as hdf:
            hdf.create_dataset("acceleration",
                               compression=compression,
                               data=data,
                               shape=(number_lines, ))


if __name__ == '__main__':
    converter = Converter("Data/Log.txt")
    converter.store_csv()
    converter.store_hdf()
    converter.store_hdf(compression="gzip")
