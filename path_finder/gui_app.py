import sys
import threading
from random import randint
from time import sleep

from PyQt5.QtCore import Qt, QRunnable, pyqtSlot, QThreadPool
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from genetic import GeneticSolver
from utils import read_from_file


class StartWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(StartWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Stratec")
        self.selected_file = None

        self.layout = QVBoxLayout()

        # load playground from csv file
        self.open_file_dialog_button = QPushButton('Load playground from csv file')
        self.open_file_dialog_button.clicked.connect(self.open_file_dialog_button_clicked)
        self.layout.addWidget(self.open_file_dialog_button)

        # load genes
        self.open_file_dialog_button = QPushButton('Load genes')
        self.open_file_dialog_button.clicked.connect(self.load_genes)
        self.layout.addWidget(self.open_file_dialog_button)

        self.setLayout(self.layout)
        self.game_windows = []

        self.open_selected_file_button = QPushButton('Open')
        self.open_selected_file_button.clicked.connect(self.load_playground_from_selected_file)

        self.threadpool = QThreadPool()

    def open_file_dialog_button_clicked(self):
        print('open_csv_file_button_clicked')
        select_file_widget = FileDialog()
        select_file_widget.open_file_name_dialog()
        select_file_widget.show()

        if select_file_widget.selected_filename:
            h_layout = QHBoxLayout()
            self.selected_file = select_file_widget.selected_filename
            h_layout.addWidget(QLabel(select_file_widget.selected_filename))
            open_selected_file_button = QPushButton('Open')
            open_selected_file_button.clicked.connect(
                lambda: self.load_playground_from_selected_file(select_file_widget.selected_filename)
            )
            h_layout.addWidget(open_selected_file_button)
            self.layout.addLayout(h_layout)
        select_file_widget.close()

    def load_playground_from_selected_file(self, file):
        matrix = read_from_file(file)
        new_game = MainWindow(matrix=matrix)
        self.game_windows.append(new_game)
        new_game.show()

    def load_genes(self):
        config = read_from_file('/Users/dan.ailenei/myprojects/Semester-6/Stratec/data/Step_One.csv')
        solver = GeneticSolver.from_config(config, generations=100, population_size=5)

        # for individual in solver.population.individuals:
        #     matrix = individual.genes.to_matrix()
        #     new_game = MainWindow(matrix=matrix)
        #     self.game_windows.append(new_game)
        #     new_game.show()

        game = MainWindow(matrix=config)
        self.game_windows.append(game)
        game.show()

        class Worker(QRunnable):
            @pyqtSlot()
            def run(self):
                for i in range(1000):
                    sleep(2)
                    game.table_widget.new_matrix_button.click()
        self.threadpool.start(Worker())



class MainWindow(QWidget):

    def __init__(self, *args, matrix=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Stratec (Almost) Path Finder")

        self.layout = QVBoxLayout()

        if not matrix:
            self.complete_path_button.setDisabled(True)
            self.next_step_button.setDisabled(True)

        if matrix:
            self.table_widget = TableWidget(matrix)
            self.layout.addWidget(self.table_widget)
        else:
            label = QLabel("Could not display table widget :(")
            label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(label)

        # save button
        self.save_configuration_button = QPushButton(text='Save configuration as csv')
        self.save_configuration_button.clicked.connect(self.save_configuration_button_clicked)
        self.layout.addWidget(self.save_configuration_button)

        self.setLayout(self.layout)

    def save_configuration_button_clicked(self):
        select_file_widget = FileDialog()
        select_file_widget.save_file_dialog()
        select_file_widget.show()
        if select_file_widget.selected_filename:
            self.table_widget.playground.save_to_csv(select_file_widget.selected_filename)


class TableWidget(QWidget):
    colors = {'0': (0, 0, 0), 0: (0, 0, 0)}

    def __init__(self, matrix):
        super(TableWidget, self).__init__()
        self.matrix = matrix
        self.table = None
        self.new_matrix_button = QPushButton(text='Dumnezeu cu mila')
        self.new_matrix_button.clicked.connect(lambda x: self.initUI([[1,2,3], [1,2,3]]))

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.initUI(matrix)

    def initUI(self, matrix):
        self.table = QTableWidget(self)
        self.table.setRowCount(len(self.matrix))
        self.table.setColumnCount(len(self.matrix[0]))

        labels = [str(i) for i in range(len(self.matrix[0]))]
        self.table.setHorizontalHeaderLabels(labels)
        self.table.setVerticalHeaderLabels(labels)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.grid.addWidget(self.table, 0, 0)
        self.show()
        self.show_numbered_pins(matrix)

    def show_numbered_pins(self, matrix):
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                self.set_item(i, j, value)

    def set_item(self, i, j, value):
        item = QTableWidgetItem(str(value))
        color = self.colors.setdefault(value, (randint(50, 125), randint(50, 125), randint(50, 125)))
        item.setBackground(QBrush(QColor(*color)))
        self.table.setItem(i, j, item)


class FileDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Dialog'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.selected_filename = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "All Files (*);;CSV Files (*.csv)", options=options)
        print(file_name)
        self.selected_filename = file_name

    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "All Files (*);;CSV Files (*.csv)", options=options)
        print(file_name)
        self.selected_filename = file_name


if __name__ == '__main__':
    filepath = '..\\2020_Internship_Challenge_Software\\Step_Two-Z.csv'
    app = QApplication(sys.argv)

    startWindow = StartWindow()
    startWindow.show()

    app.exec_()
