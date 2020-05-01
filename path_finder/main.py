import asyncio
import os

from genetic import GeneticSolver
from gui_app import SgMatrixes
from utils import read_from_file, get_random_color, get_random_color_async
import PySimpleGUI as sg

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WINDOWS = 6


async def load_genes(window):
    while True:
        event, values = window.read(timeout=1)
        if event in (None, 'Exit'):
            break
        if event != '__TIMEOUT__':
            print(f'[{event}] [{values}]')
        await asyncio.sleep(0.0001)


async def compute_matrixes(matrix, window, key):
    solver = GeneticSolver.from_config(matrix, generations=100, population_size=200)
    async for individual in solver.population.async_individuals_generator():
        for i, row in enumerate(individual.genes.to_matrix()):
            for j, elem in enumerate(row):
                window[(i, j, key)].update(elem, button_color=('#F0F0F0', get_random_color(elem)))
        await asyncio.sleep(0.0001)


async def main():
    dir = os.path.dirname(BASE_DIR)
    config = read_from_file(os.path.join(dir, 'data', 'Step_One.csv'))
    new_game = SgMatrixes(config, WINDOWS)
    window = sg.Window('Cell madness', new_game).Finalize()
    window.Maximize()

    courutines = [compute_matrixes(config, window, i) for i in range(1, WINDOWS + 1)]
    await asyncio.wait([load_genes(window)] + courutines)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
