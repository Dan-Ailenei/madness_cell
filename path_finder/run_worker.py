import sys
from genetic import GeneticSolver
from utils import read_from_file


def run_worker():
    config = read_from_file(path_to_file)
    solver = GeneticSolver.from_config(config, generations=100, population_size=200)
    for individual in solver.population.individuals:
        matrix = individual.genes.to_matrix()
        print(matrix, file=sys.stderr)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path_to_file, key = sys.argv[1:]
    else:
        path_to_file = '/Users/dan.ailenei/myprojects/Semester-6/Stratec/data/Step_One.csv'
    run_worker()
