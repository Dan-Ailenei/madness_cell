import copy
from collections import defaultdict

from cached_property import cached_property


class LabeledSparseMatrix:
    def __init__(self, number_of_paths, size):
        self.number_of_paths = number_of_paths
        self.size = size
        self.data = {}

    def copy(self):
        instance = copy.copy(self)
        instance.data = {}
        return instance


class Genes:
    # read only
    start_points = None
    item_to_points = None

    def __init__(self, labeled_sparse_matrix):
        self.paths = defaultdict(list)
        self.labeled_sparse_matrix = labeled_sparse_matrix

    def __contains__(self, key):
        return key in self.labeled_sparse_matrix.data or key in self.start_points

    def __getitem__(self, key):
        if key in self.labeled_sparse_matrix.data:
            return self.labeled_sparse_matrix.data[key]
        return self.start_points[key]

    def __setitem__(self, point, number):
        self.labeled_sparse_matrix.data[point] = number

    def delete_old_path(self, key):
        if key in self.paths:
            del self.paths[key]

    @cached_property
    def get_first_points_in_paths(self):
        return {path[0] for path in self.paths}

    @classmethod
    def set_start_points(cls, config):
        cls.start_points = cls.__get_start_points(config)
        cls.item_to_points = cls.__item_to_coord_start_coords()

    @classmethod
    def __item_to_coord_start_coords(cls):
        rez = defaultdict(list)
        for coord, num in cls.start_points.items():
            rez[num].append(coord)
        return rez

    @classmethod
    def __get_start_points(cls, config):
        return {
            (i, j): int(cell)
            for i, line in enumerate(config)
            for j, cell in enumerate(line)
            if cell != '0'
        }

    def copy(self):
        instance = copy.copy(self)
        instance.labeled_sparse_matrix = instance.labeled_sparse_matrix.copy()
        instance.paths = []
        return instance

    def to_matrix(self):
        k, l = self.labeled_sparse_matrix.size
        rez = []
        for i in range(k):
            current_list = []
            rez.append(current_list)
            for j in range(l):
                if (i, j) in self.labeled_sparse_matrix.data:
                    current_list.append(self.labeled_sparse_matrix.data[(i, j)])
                elif (i, j) in self.start_points:
                    current_list.append(self.start_points[(i, j)])
                else:
                    current_list.append(0)
        return rez

    def print_matrix(self, bad_points):
        matrix = self.to_matrix()
        print("-" * len(matrix[0]))
        for i, line in enumerate(matrix):
            rez = ''
            for j, e in enumerate(line):
                if (i, j) in bad_points:
                    rez += 'X, '
                else:
                    rez += f'{e}, '
            print(rez[:-2])
        print("-" * len(matrix[0]))
