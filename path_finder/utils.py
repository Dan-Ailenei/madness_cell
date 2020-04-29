import csv


def read_from_file(file):
    with open(file) as f:
        reader = csv.reader(f, delimiter=",")
        return list(reader)
