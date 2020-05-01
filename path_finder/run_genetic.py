#!/Users/dan.ailenei/myprojects/Semester-6/Stratec/venv/bin/ python

import os

from genetic import GeneticSolver
from utils import read_from_file
import sys

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config = read_from_file('/Users/dan.ailenei/myprojects/Semester-6/Stratec/data/Step_One.csv')
solver = GeneticSolver.from_config(config, generations=100, population_size=200)

print(sys.argv)
