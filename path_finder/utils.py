import csv
from random import randint
import math

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


def distance(x, y):
    # don t compute the actual full distance
    x1, y1 = x
    x2, y2 = y
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
