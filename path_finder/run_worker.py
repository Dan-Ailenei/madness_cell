import sys
from genetic import GeneticSolver
from utils import read_from_file


def run_worker():
    config = read_from_file(path_to_file)
    solver = GeneticSolver.from_config(config, generations=100, population_size=200)
    for i, individual in enumerate(solver.population.individuals):
        matrix = individual.genes.to_matrix()
        print(matrix, file=sys.stderr)


if __name__ == '__main__':
    path_to_file, key = sys.argv[1:]
    run_worker()
