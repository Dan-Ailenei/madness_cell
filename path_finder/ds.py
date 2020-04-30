import copy
import csv
from collections import defaultdict


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
    def __init__(self, labeled_sparse_matrix, start_coords):
        self.paths = []
        self.start_coords = start_coords
        self.labeled_sparse_matrix = labeled_sparse_matrix

    def __contains__(self, key):
        return key in self.labeled_sparse_matrix.data or key in self.start_coords

    def __getitem__(self, key):
        if key in self.labeled_sparse_matrix.data:
            return self.labeled_sparse_matrix.data[key]
        return self.start_coords[key]

    def __setitem__(self, indexes, number):
        self.labeled_sparse_matrix.data[indexes] = number
        self.paths[number - 1].append(indexes)

    @classmethod
    def item_to_coord_start_coords(cls, start_coords):
        rez = defaultdict(list)
        for coord, num in start_coords.items():
            rez[num].append(coord)
        return rez

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
                elif (i, j) in self.start_coords:
                    current_list.append(self.start_coords[(i, j)])
                else:
                    current_list.append(0)
        return rez

    def write_to_file(self):
        with open('/Users/dan.ailenei/myprojects/Semester-6/Stratec/data/genes.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for row in self.to_matrix():
                writer.writerow(row)
