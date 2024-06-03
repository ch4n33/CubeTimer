from PyQt5.QtWidgets import \
    QVBoxLayout, QWidget

# for plotting cube status
from cube import Cube
from formula import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        
        # Create a figure and add a plot
        self.figure = Figure(tight_layout=True,)
        self.canvas = FigureCanvas(self.figure)
        
        # Layout to add the canvas
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        
        # Draw something on the canvas
        self.plot()

    def plot(self, cube_type=3, formula=None):
        # Clear the figure
        self.figure.clear()
        
        # Add a subplot and plot the data
        ax = self.figure.add_subplot()
        cube = Cube(cube_type)
        cube.attempt_formula(formula)
        cube.plot(self.figure, ax)
        
        # Modify the background color of the figure
        self.figure.patch.set_facecolor('none')
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        
        self.canvas.draw()
    
    def update_plot(self, cube_type, formula):
        print('update plot : ', str(formula))
        self.plot(cube_type, formula)
