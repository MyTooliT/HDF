# -- Imports ------------------------------------------------------------------

from csv import DictWriter
from pathlib import Path
from re import compile

from h5py import File
from numpy import asarray, recarray

# -- Functions ----------------------------------------------------------------


def read_log(filepath):
    """Read acceleration log data"""

    line_regex = compile(r"\[I\]\s*\((?P<ms>\d+)ms\)[^\d]+(?P<counter>\d+)"
                         r"[^\d]+(?P<timestamp>\d+(\.\d+)?)[^\d]+"
                         r"(?P<acceleration>\d+);")
    values = []
    with open(filepath) as file:
        for line in file:
            match = line_regex.match(line)
            if match:
                values.append({
                    'millisecond': match['ms'],
                    'counter': match['counter'],
                    'timestamp': match['timestamp'],
                    'acceleration': match['acceleration']
                })

    return values


def convert_values_rows(values):
    """Return acceleration data as rows (instead of lines)"""

    miliseconds = []
    counters = []
    timestamps = []
    acceleration = []
    for value in values:
        miliseconds.append(value['millisecond'])
        counters.append(value['counter'])
        timestamps.append(value['timestamp'])
        acceleration.append(value['acceleration'])

    return {
        'millisecond': miliseconds,
        'counter': counters,
        'timestamp': timestamps,
        'acceleration': acceleration
    }


def convert_csv(filepath, values):
    """Store acceleration data in CSV file"""

    with open(Path(filepath).with_suffix(".csv"), 'w', newline='') as csvfile:
        fieldnames = ['millisecond', 'counter', 'timestamp', 'acceleration']
        writer = DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(values)


def convert_hdf(filepath, values):
    """Store acceleration data in HDF5 file"""

    types = [('millisecond', int), ('counter', int), ('timestamp', float),
             ('acceleration', int)]
    number_lines = len(values['millisecond'])
    data = recarray(number_lines, dtype=types)
    data['millisecond'] = asarray(values['millisecond'])
    data['counter'] = asarray(values['counter'])
    data['timestamp'] = asarray(values['timestamp'])
    data['acceleration'] = asarray(values['acceleration'])
    with File(Path(filepath).with_suffix(".hfd5"), 'w') as hdf:
        hdf.create_dataset("acceleration", data=data, shape=(number_lines, ))


if __name__ == '__main__':
    filepath = "Data/Log.txt"
    values = read_log(filepath)
    convert_csv(filepath, values)
    convert_hdf(filepath, convert_values_rows(values))
