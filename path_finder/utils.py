import csv
from random import randint

colors = {}


def read_from_file(file):
    with open(file) as f:
        reader = csv.reader(f, delimiter=",")
        return list(reader)


def get_random_color(item):
    return colors.setdefault(
        item,
        '#%02X%02X%02X' % (randint(50, 125), randint(50, 125), randint(50, 125))
    )
