import PySimpleGUI as sg

from utils import get_random_color


def MatrixElement(i, j, windows, elem=None):
    text = elem if elem and elem != '0' else 0
    return sg.Button(text, size=(1, 1), key=(i, j, windows), pad=(1, 1), button_color=('#F0F0F0', get_random_color(elem)))


def ButtonMatrix(matrix, windows):
    return [
        sg.Column([
            [MatrixElement(i, j, windows, elem if windows > 0 else None) for j, elem in enumerate(row)]
            for i, row in enumerate(matrix)
        ])
    ]


def SgMatrixes(matrix, windows):
    ROW_SIZE = 2
    COLUMN_SIZE = 3

    arena = []

    for i in range(COLUMN_SIZE):
        col = []
        for j in range(ROW_SIZE):
            col.append(ButtonMatrix(matrix, windows))
            windows -= 1
        arena.append(sg.Column(col))
    return [arena]
