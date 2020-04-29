import copy
import csv


class LabeledSparseMatrix:
    def __init__(self, number_of_paths, size, start_coords):
        self.number_of_paths = number_of_paths
        self.start_coords = start_coords
        self.size = size
        self.data = {}

    def _get_start_coords(self, config, number_of_paths):
        return {
            (i, j): int(cell)
            for i, line in enumerate(config)
            for j, cell in enumerate(line)
            if cell != '0'
        }

    def copy(self):
        instance = copy.copy(self)
        instance.data = {}
        return instance

    def __contains__(self, key):
        return key in self.data or key in self.start_coords

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        return self.start_coords[key]

    def to_matrix(self):
        k, l = self.size
        rez = []
        for i in range(k):
            current_list = []
            rez.append(current_list)
            for j in range(l):
                if (i, j) in self.data:
                    current_list.append(self.data[(i, j)])
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
