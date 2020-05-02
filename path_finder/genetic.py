import asyncio
import random
from itertools import product
from random import randint

from cached_property import cached_property

from ds import LabeledSparseMatrix, Genes
from utils import read_from_file, distance


class GeneticSolver:
    def __init__(self, **kwargs):
        self.population_size = kwargs.pop('population_size', 100)
        self.generations = kwargs.pop('generations', 500)

    @classmethod
    def from_config(cls, config, **kwargs):
        solver = cls(**kwargs)
        number_of_paths = int(max(sum(config, [])))
        Genes.set_start_points(config)

        size = (len(config), len(config[0]))
        labeled_sparse_matrix = LabeledSparseMatrix(number_of_paths, size)

        solver.population = Population.initialized_population(
            solver.population_size,
            labeled_sparse_matrix,
        )
        return solver

    def solve(self):
        aux_population = Population(self.population.size)

        for _ in range(self.generations):
            for __ in range(len(self.population.individuals) // 2):
                p1, p2 = self.population.selection()
                o1, o2 = p1.crossover(p2)
                o3 = o1.mutate()
                o4 = o2.mutate()

                xx = [p1, p2, o1, o2, o3, o4]
                xx.sort()

                aux_population.add(xx[0])
                aux_population.add(xx[1])

            self.population = aux_population
            aux_population = Population(self.population_size)
        return max(self.population.individuals).genes


class Individual:
    def __init__(self, genes):
        self.genes = genes

    def crossover(self, p2):
        pass

    def mutate(self):
        pass

    @cached_property
    def fitness(self):
        score = 0
        first_points_in_paths = self.genes.first_points_in_paths

        for point in self.genes.start_points:
            if point in self.genes.labeled_sparse_matrix.data and point not in first_points_in_paths:
                score += 5

        # for
        # distance()

        return score

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
    def initialized_population(cls, size, labeled_sparse_matrix):
        population = cls(size)
        population.initialize(size, labeled_sparse_matrix)
        return population

    def initialize(self, size, labeled_sparse_matrix):
        k, l = labeled_sparse_matrix.size
        unique_numbers = list(range(1, labeled_sparse_matrix.number_of_paths + 1))
        start_points = Genes.start_points
        number_of_current_cells = len(start_points)
        cells_to_initialize_for_each_path = (k * l - number_of_current_cells) // 2

        for _ in range(size):
            genes = Genes(labeled_sparse_matrix.copy())
            random.shuffle(unique_numbers)
            for number in unique_numbers:
                current_number_points = list(genes.item_to_points[number])
                random.shuffle(current_number_points)
                for point in current_number_points:
                    self.generate_random_path(point, genes, cells_to_initialize_for_each_path)

            self.individuals.append(Individual(genes))

    def generate_random_path(self, starting_point, genes, number_of_points_for_path):
        genes.delete_old_path(starting_point)
        number = genes[starting_point]
        current_point = starting_point

        for _ in range(randint(1, number_of_points_for_path)):
            neighbours = self._index_neighbours(*current_point)

            point = random.sample(neighbours, 1)[0]
            if point in genes.item_to_points[number]:
                genes[point] = number
                genes.paths[starting_point].append(point)
                break
            if point not in genes and self._space_condition(genes, point, number):
                genes[point] = number
                genes.paths[starting_point].append(point)
                current_point = point

    def _space_condition(self, genes, indexes, number):
        return all(neighbour not in genes or genes[neighbour] == number for neighbour in self._index_neighbours(*indexes))

    def _index_neighbours(self, i, j):
        return set(product([i - 1, i, i + 1], [j - 1, j, j + 1])) - {(i, j)}

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
    solver.solve()
