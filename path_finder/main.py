import asyncio
import json
import os
import sys
from gui_app import SgMatrixes
from utils import read_from_file, get_random_color
import PySimpleGUI as sg

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WINDOWS = 6


async def block_queue(window):
    while True:
        # apparently this function renders the changes
        window.read(timeout=0)
        await asyncio.sleep(0.1)


async def receive_signals(window, proc, key):
    number = 0
    while True:
        data = await proc.stderr.readline()
        proc.communicate()
        message = data.decode('ascii').rstrip()
        if not message:
            break
        matrix = json.loads(message)
        for i, row in enumerate(matrix):
            for j, elem in enumerate(row):
                window[(i, j, key)].update(elem, button_color=('#F0F0F0', get_random_color(elem)))
        number += 1
        # maybe we can remove this, atm is too fast
        await asyncio.sleep(0.1)
    # Wait for the subprocess exit.
    await proc.wait()


async def main():
    dir = os.path.dirname(BASE_DIR)
    file_path = os.path.join(dir, 'data', 'Step_One.csv')
    config = read_from_file(file_path)
    new_game = SgMatrixes(config, WINDOWS)
    window = sg.Window('Cell madness', new_game).Finalize()
    window.Maximize()
    coroutines = []
    for i in range(1, WINDOWS + 1):
        proc = await asyncio.create_subprocess_exec(
            sys.executable, f"{os.path.join(dir, 'path_finder', 'run_worker.py')}",
            file_path,
            str(i),
            stderr=asyncio.subprocess.PIPE
        )
        coroutines.append(receive_signals(window, proc, i))

    await asyncio.wait([block_queue(window)] + coroutines)
    window.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
