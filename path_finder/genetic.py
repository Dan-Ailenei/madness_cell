import random
from itertools import product
from random import randint

from ds import LabeledSparseMatrix, Genes
from utils import read_from_file


class GeneticSolver:
    def __init__(self, **kwargs):
        self.population_size = kwargs.pop('population_size', 100)
        self.generations = kwargs.pop('generations', 500)

    @classmethod
    def from_config(cls, config, **kwargs):
        solver = cls(**kwargs)
        number_of_paths = int(max(sum(config, [])))
        start_coords = solver._get_start_coords(config)
        size = (len(config), len(config[0]))
        labeled_sparse_matrix = LabeledSparseMatrix(number_of_paths, size)

        solver.population = Population.initialized_population(
            solver.population_size,
            labeled_sparse_matrix,
            start_coords
        )
        return solver

    def _get_start_coords(self, config):
        return {
            (i, j): int(cell)
            for i, line in enumerate(config)
            for j, cell in enumerate(line)
            if cell != '0'
        }

    def solve(self):
        self.population.eval()
        aux_population = Population(self.population.size)

        for _ in range(self.generations):
            for __ in range(len(self.population.individuals) // 2):
                p1, p2 = self.population.selection()
                o1, o2 = p1.crossover(p2)
                o1.mutate()
                o2.mutate()

                o1.eval()
                o2.eval()
                xx = [p1, p2, o1, o2]
                xx.sort()

                aux_population.add(xx[0])
                aux_population.add(xx[1])

            self.population = aux_population
            aux_population = Population(self.population_size)
        return min(self.population.individuals).genes


class Individual:
    def __init__(self, labeled_sparsed_matrix):
        self.genes = labeled_sparsed_matrix

    def crossover(self, p2, codo):
        pass

    def mutate(self):
        pass

    def eval(self, codo):
        self.fitness = codo[int(self.genes, 2)]

    def __str__(self):
        return str(self.genes)+" "+str(self.fitness)

    def __lt__(self, other):
        return self.fitness < other.fitness


class Population:
    def __init__(self, size):
        self.individuals = []
        self.size = size
        self.size_turnir = size // 5

    @classmethod
    def initialized_population(cls, size, labeled_sparse_matrix, start_coords):
        population = cls(size)
        population.initialize(size, labeled_sparse_matrix, start_coords)
        return population

    def initialize(self, size, labeled_sparse_matrix, start_coords):
        k, l = labeled_sparse_matrix.size
        unique_numbers = range(1, labeled_sparse_matrix.number_of_paths + 1)
        initial_points = set(start_coords)
        number_of_current_cells = len(initial_points)
        cells_to_initialize = (k * l - number_of_current_cells) // 2
        cells_to_initialize_for_each_path = cells_to_initialize // number_of_current_cells

        items_to_coords = Genes.item_to_coord_start_coords(start_coords)

        for _ in range(size):
            wrong_generated_cell = 0
            genes = Genes(labeled_sparse_matrix.copy(), start_coords)

            for number in unique_numbers:
                current_number_pins = items_to_coords[number]
                random_start = current_number_pins[randint(0, len(current_number_pins) - 1)]
                current_path = [random_start]
                genes.paths.append(current_path)

                for __ in range(cells_to_initialize_for_each_path):
                    neighbours = self._index_neighbours(*current_path[-1])

                    indexes = random.sample(neighbours, 1)[0]
                    if indexes not in genes and self._space_condition(genes, indexes, number):
                        genes[indexes] = number
                    else:
                        wrong_generated_cell += 1

            self.individuals.append(Individual(genes))
            print(f'There were {wrong_generated_cell} wrong generated cells, population size: {self.size}')

    def _space_condition(self, genes, indexes, number):
        return all(neighbour not in genes or genes[neighbour] == number for neighbour in self._index_neighbours(*indexes))

    def _index_neighbours(self, i, j):
        return set(product([i - 1, i, i + 1], [j - 1, j, j + 1])) - {(i, j)}

    def eval(self):
        for individ in self.individuals:
            individ.eval()

    def selection(self):
        individual1, index = self._selection()
        return individual1, self._selection(excluded=index)[0]

    def _selection(self, excluded=None):
        i = 0
        turnir = []
        while i < self.size_turnir:
            index = randint(0, self.size - 1)
            if excluded is not None and index == excluded:
                continue
            turnir.append((self.individuals[index], index))
            i += 1

        return max(turnir)

    def add(self, o):
        self.individuals.append(o)


if __name__ == '__main__':
    config = read_from_file('/Users/dan.ailenei/myprojects/Semester-6/Stratec/data/Step_One.csv')
    solver = GeneticSolver.from_config(config, generations=100, population_size=200)
