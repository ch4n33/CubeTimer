import sys
import random
import pycuber as pc
from scramble import Scramble
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,\
        QVBoxLayout, QLabel, QWidget, \
        QComboBox, QLineEdit, QTextEdit, \
        QGridLayout, QInputDialog 

from PyQt5.QtCore import Qt, QTimer, QTime

class CubeTimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.time = QTime(0, 0)
        self.timer_running = False
        self.config = {}
        
        self.setWindowTitle('Cube Timer')
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QGridLayout(self.central_widget)
        
        # 큐브 종류 선택
        self.cube_type_label = QLabel('Select Cube Type:', self)
        self.layout.addWidget(self.cube_type_label, 0, 0)
        
        self.cube_type_combo = QComboBox(self)
        self.cube_type_combo.addItems(['2x2', '3x3', '4x4', '5x5'])
        self.layout.addWidget(self.cube_type_combo, 0, 1)
        
        # 스크램블 생성 버튼
        self.scramble_button = QPushButton('Generate Scramble', self)
        self.scramble_button.clicked.connect(self.generate_scramble)
        self.layout.addWidget(self.scramble_button, 1, 0, 1, 2)
        
        # 스크램블 표시
        self.scramble_label = QLabel('Scramble:', self)
        self.layout.addWidget(self.scramble_label, 2, 0)
        
        self.scramble_text = QLabel('', self)
        self.layout.addWidget(self.scramble_text, 2, 1)
        
        # # 타이머 시작 버튼
        # self.start_timer_button = QPushButton('Start Timer', self)
        # self.layout.addWidget(self.start_timer_button, 3, 0, 1, 2)
        # self.start_timer_button.clicked.connect(self.timer)
        
        # 타이머 기록
        self.timer_state = QLabel('Timer', self)
        self.layout.addWidget(self.timer_state, 3, 0)
        
        self.time_display = QLabel("00:00:000", self)
        self.layout.addWidget(self.time_display, 3, 1)
        
        self.timer_save_button = QPushButton('Save Time', self)
        self.layout.addWidget(self.timer_save_button, 3, 2)
        self.timer_save_button.clicked.connect(self.save_time)
        
        # 태그 입력
        self.tag_label = QLabel('Tag:', self)
        self.layout.addWidget(self.tag_label, 4, 0)
        
        self.tag_input = QLineEdit(self)
        self.layout.addWidget(self.tag_input, 4, 1)
        
        # 이력 표시
        self.history_label = QLabel('History:', self)
        self.layout.addWidget(self.history_label, 5, 0)
        
        self.history_text = QTextEdit(self)
        self.history_text.setReadOnly(True)
        self.layout.addWidget(self.history_text, 5, 1)
        
        # 초기 설정 로드
        self.load_config()
        
        # 설정 변경은 아직 구현하지 않았습니다.
        
        # 초기 이력 로드
        self.load_history(self.config['history_directory']+self.config['default_tag'])
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
        cube_type = self.cube_type_combo.currentText()
        scramble = self.get_scramble(cube_type)
        self.scramble_text.setText(scramble)
        
    def get_scramble(self, cube_type):
        # 여기서 스크램블을 생성하는 로직을 구현합니다.
        if cube_type == '3x3':
            cube = pc.Cube()
            scramble = pc.Formula()
            scramble.random(25)
            return str(scramble)
        else:
            self.scrambler = Scramble()
            scramble = self.scrambler.get(int(cube_type[0]))
            return str(scramble)
        
    def load_history(self, tag):
        # 이력 로드
        try:
            with open(tag, 'r') as file:
                history = file.read().split('\n')
                firstline = history.pop(0)
                cubeInfo = firstline
                match cubeInfo:
                    case "2x2":
                        self.cube_type_combo.setCurrentIndex(0)
                    case "3x3":
                        self.cube_type_combo.setCurrentIndex(1)
                    case "4x4":
                        self.cube_type_combo.setCurrentIndex(2)
                    case "5x5":
                        self.cube_type_combo.setCurrentIndex(3)
                    case _:
                        print("No match")
                        raise ValueError("Invalid cube type found in history.")
                self.history_text.setText('\n'.join(history))
        except FileNotFoundError:
            self.history_text.setText('No history found.')
        except ValueError as e:
            self.history_text.setText('Error loading history: ' + str(e))
            
    def save_history(self, entry, tag):
        with open(tag, 'a') as file:
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
            self.timer_running = False
            self.stop_timer()
        else:
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
        self.save_history(entry, self.config['history_directory']+self.config['default_tag'])
        self.reset_timer()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CubeTimerApp()
    window.show()
    sys.exit(app.exec_())