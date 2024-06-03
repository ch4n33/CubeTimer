import sys
import random
import pycuber as pc
import statistics as stat
from scramble import Scramble

from util import parse_time, format_time
from PyQt5.QtWidgets import \
    QApplication, QMainWindow, QPushButton,\
    QVBoxLayout, QLabel, QWidget, \
    QComboBox, QLineEdit, QTextEdit, \
    QGridLayout, QInputDialog 
from PyQt5.QtCore import Qt, QTimer, QTime

# for plotting cube status
from cube import Cube
from formula import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class SelectTagDialog(QInputDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Select Tag')
        self.setLabelText('Enter a tag for this session:')
        self.setOkButtonText('Select')
        self.setCancelButtonText('Cancel')
        self.setInputMode(QInputDialog.TextInput)
        self.setTextValue('default')
        
        self.ui_select_cube_type()
        self.show()

    def getText(self):
        return self.textValue()
            
    def ui_select_cube_type(self):
        # 큐브 종류 선택
        self.cube_type_label = QLabel('Select Cube Type:', self)
        self.layout.addWidget(self.cube_type_label, 0, 0)
        
        self.cube_type_combo = QComboBox(self)
        self.cube_type_combo.addItems(['2x2', '3x3', '4x4', '5x5'])
        self.layout.addWidget(self.cube_type_combo, 0, 1)


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        
        # Create a figure and add a plot
        self.figure = Figure()
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
        cube = Cube(3)
        cube.attempt_formula(formula)
        cube.plot(ax)
        
        self.canvas.draw()
    
    def update_plot(self, cube_type, formula):
        print('update plot : ', str(formula))
        self.plot(cube_type, formula)


class CubeTimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.time = QTime(0, 0)
        self.timer_running = False
        self.config = {}
        self.initUI()
        self.init_data()
    
    def initUI(self):    
        self.setWindowTitle('Cube Timer')
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QGridLayout(self.central_widget)
        
        self.ui_scramble()
        self.ui_timer()
        self.ui_history()

    
    def ui_scramble(self):
        # 스크램블 생성 버튼
        self.scramble_button = QPushButton('Generate Scramble', self)
        self.scramble_button.clicked.connect(self.generate_scramble)
        self.layout.addWidget(self.scramble_button, 0, 1)
        
        # 스크램블 표시
        self.scramble_label = QLabel('Scramble:', self)
        self.layout.addWidget(self.scramble_label, 1, 0)
        
        self.scramble_text = QLabel('', self)
        self.layout.addWidget(self.scramble_text, 1, 1)
        
        self.cube_show_widget = MatplotlibWidget(self)
        self.layout.addWidget(self.cube_show_widget, 2,0, 2,1)
    
    def ui_timer(self):    
        # # 타이머 시작 버튼
        # self.start_timer_button = QPushButton('Start Timer', self)
        # self.layout.addWidget(self.start_timer_button, 3, 0, 1, 2)
        # self.start_timer_button.clicked.connect(self.timer)
        
        # 타이머 기록
        self.timer_state = QLabel('Timer', self)
        self.layout.addWidget(self.timer_state, 3, 0)
        
        self.time_display = QLabel("00:00:000", self)
        self.layout.addWidget(self.time_display, 3, 1)
        
        self.timer_save_button = QPushButton('Reset Time', self)
        self.layout.addWidget(self.timer_save_button, 3, 2)
        self.timer_save_button.clicked.connect(self.save_time)
    
    def ui_history(self):
        # 태그 입력
        self.tag_label = QLabel('Tag:', self)
        self.layout.addWidget(self.tag_label, 4, 0)
        
        self.tag_text = QLineEdit(self)
        self.tag_text.setReadOnly(True)
        self.layout.addWidget(self.tag_text, 4, 1)
        
        # 통계 표시
        self.mean_label = QLabel('Mean:', self)
        self.layout.addWidget(self.mean_label, 5, 0)
        
        self.mean_text = QLineEdit(self)
        self.mean_text.setReadOnly(True)
        self.layout.addWidget(self.mean_text, 5, 1)
        
        self.std_label = QLabel('Std Dev:', self)
        self.layout.addWidget(self.std_label, 6, 0)
        
        self.std_text = QLineEdit(self)
        self.std_text.setReadOnly(True)
        self.layout.addWidget(self.std_text, 6, 1)
        
        # 이력 표시
        self.history_label = QLabel('History:', self)
        self.layout.addWidget(self.history_label, 7, 0)
        
        self.history_text = QTextEdit(self)
        self.history_text.setReadOnly(True)
        self.layout.addWidget(self.history_text, 7, 1, 7, 2)
        
    
    def init_data(self): 
        # 초기 설정 로드
        self.load_config()
        
        # 설정 변경은 아직 구현하지 않았습니다.
        
        # 초기 이력 로드
        self.load_history((self.config['history_directory'], self.config['default_tag']))
        self.generate_scramble()
        
    def load_config(self):
        config = {}
        try:
            with open('config.txt', 'r') as file:
                for line in file:
                    key,value = line.strip().split('=')
                    print('config :',key, value)
                    config[key] = value
                self.config = config
        except FileNotFoundError:
            return 'No config file found.'
        
    def save_config(self):
        with open('config.txt', 'w') as file:
            for key, value in self.config.items():
                file.write(f"{key}={value}\n")
    
    def generate_scramble(self):
        scramble = self.get_scramble(self.cube_type)
        self.scramble_text.setText(scramble)
        
    def get_scramble(self, cube_type):
        # 여기서 스크램블을 생성하는 로직을 구현합니다.
        self.scrambler = Scramble()
        scramble = self.scrambler.get(int(cube_type))
        self.cube_show_widget.update_plot(cube_type, scramble)
        return str(scramble)
        
    def load_history(self, tag):
        # 이력 로드
        dir = './'.join(tag)
        try:
            with open(dir, 'r') as file:
                history = file.read().split('\n')
                firstline = history.pop(0)
                cubeInfo = firstline
                match cubeInfo:
                    case "2x2":
                        self.cube_type = 2
                    case "3x3":
                        self.cube_type = 3
                    case "4x4":
                        self.cube_type = 4
                    case "5x5":
                        self.cube_type = 5
                    case _:
                        print("No match")
                        raise ValueError("Invalid cube type found in history.")
                self.history_text.setText('\n'.join(history))
                self.tag_text.setText(tag[-1])
        except FileNotFoundError:
            self.history_text.setText('No history found.')
        except ValueError as e:
            self.history_text.setText('Error loading history: ' + str(e))
        
        self.statistics_update()
            
    def save_history(self, entry, tag):
        dir = './'.join(tag)
        with open(dir, 'a') as file:
            file.write(entry + '\n')
        self.load_history(tag)
        
    def keyPressEvent(self, e): #키가 눌러졌을 때 실행됨
        # space bar is pressed
        if e.key() == Qt.Key_Space:
            self.timer_toggle()

    def keyReleaseEvent(self,e): #키를 누른상태에서 뗐을 때 실행됨
        #space bar is released
        if e.key() == Qt.Key_Space:
            self.timer_toggle()

    def timer_toggle(self):
        if self.timer_running:
            self.timer_save_button.setEnabled(True)
            self.timer_running = False
            self.stop_timer()
        else:
            self.timer_save_button.setEnabled(False)
            self.timer_running = True
            self.start_timer()
        
    def start_timer(self):
        self.timer.start(1)

    def stop_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.time = QTime(0, 0)
        self.time_display.setText("00:00:000")
        self.generate_scramble()

    def update_time(self):
        self.time = self.time.addMSecs(1)
        self.time_display.setText(self.time.toString("mm:ss:zzz"))
    
    def save_time(self):
        time = self.time_display.text()
        scramble = self.scramble_text.text()
        entry = f"{time} - {scramble}"
        self.save_history(
            entry, 
            (self.config['history_directory'], self.config['default_tag'])
        )
        self.reset_timer()
        
    def statistics_update(self):
        # 통계 업데이트
        timelist = [parse_time(entry.split(' - ')[0]) for entry in self.history_text.toPlainText().split('\n')]
        timelist = [time for time in timelist if time is not None]
        
        mean, std = stat.mean(timelist), stat.stdev(timelist)
        print(timelist)
        print(mean, std)
        self.mean_text.setText(format_time(mean))
        self.std_text.setText(format_time(std))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CubeTimerApp()
    window.show()
    sys.exit(app.exec_())