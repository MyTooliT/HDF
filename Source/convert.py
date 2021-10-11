# -- Imports ------------------------------------------------------------------

from csv import DictWriter
from pathlib import Path
from re import compile

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


def convert_csv(filepath, values):
    """Convert acceleration data to CSV file"""

    with open(Path(filepath).with_suffix(".csv"), 'w', newline='') as csvfile:
        fieldnames = ['millisecond', 'counter', 'timestamp', 'acceleration']
        writer = DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(values)


if __name__ == '__main__':
    filepath = "Data/Log.txt"
    values = read_log(filepath)
    convert_csv(filepath, values)
