import statistics as stat
from .cube import Scramble
from .plot_widget import MatplotlibWidget
from .dialog import SelectRecordDialog
from .util import parse_time, format_time, get_app_data_path, ensure_app_data_directory
# TODO appdata 또는 home directory에 history 파일을 저장하도록 수정하세요.

from PyQt5.QtWidgets import \
    QMainWindow, QPushButton, QLabel,\
    QWidget, QLineEdit, QTextEdit, \
    QGridLayout
from PyQt5.QtCore import Qt, QTimer, QTime, QEvent


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
        self.setGeometry(100, 100, 500, 800)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QGridLayout(self.central_widget)
        
        self.ui_timer()
        self.ui_scramble()
        self.ui_history()
        
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 2)
        self.layout.setColumnStretch(2, 1)
        self.layout.setRowStretch(2, 1)
        self.layout.setRowStretch(7, 1)
    
    def ui_scramble(self):
        # 스크램블 생성 버튼
        self.scramble_button = QPushButton('Generate Scramble', self)
        self.scramble_button.clicked.connect(self.generate_scramble)
        self.scramble_button.setFocusPolicy(Qt.NoFocus)
        self.layout.addWidget(self.scramble_button, 0, 1)
        
        # 스크램블 표시
        self.scramble_label = QLabel('Scramble:', self)
        self.layout.addWidget(self.scramble_label, 1, 0)
        
        self.scramble_text = QLabel('', self)
        self.layout.addWidget(self.scramble_text, 1, 1)
        
        self.cube_show_widget = MatplotlibWidget(self)
        self.cube_show_widget.setFixedSize(400, 300)  # Adjust this size as needed
        self.layout.addWidget(self.cube_show_widget, 2,1, 2,2)
    
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
        self.timer_save_button.setStyleSheet("margin-left: 70px;")
        self.timer_save_button.setMaximumWidth(160)
        self.timer_save_button.setMinimumHeight(30)
        self.timer_save_button.setFocusPolicy(Qt.NoFocus)
        self.layout.addWidget(self.timer_save_button, 3, 1)
        self.timer_save_button.clicked.connect(self.reset_timer)
    
    def ui_history(self):
        # 태그 입력
        width = 80
        width_history = 600
        height = 300
        self.record_label = QLabel('Record:', self)
        self.layout.addWidget(self.record_label, 4, 0)
        
        self.record_text = QLineEdit(self)
        self.record_text.setFixedWidth(width)  # Adjust width as needed
        self.record_text.setReadOnly(True)
        self.layout.addWidget(self.record_text, 4, 1)
        
        self.select_record_button = QPushButton('Select Record', self)
        self.select_record_button.setStyleSheet("margin-left: 100px;")
        self.select_record_button.setMaximumWidth(160)
        self.layout.addWidget(self.select_record_button, 4, 1)
        self.select_record_button.clicked.connect(self.select_record)
        
        # 통계 표시
        self.mean_label = QLabel('Mean:', self)
        self.layout.addWidget(self.mean_label, 5, 0)
        
        self.mean_text = QLineEdit(self)
        self.mean_text.setFixedWidth(width)  # Adjust width as needed
        self.mean_text.setReadOnly(True)
        self.layout.addWidget(self.mean_text, 5, 1)
        
        self.mean5_label = QLabel('Recent 5:', self)
        self.mean5_label.setStyleSheet("margin-left: 100px;")
        self.layout.addWidget(self.mean5_label, 5, 1)
                              
        self.mean5_text = QLineEdit(self)
        self.mean5_text.setStyleSheet("margin-left: 170px;")
        self.mean5_text.setFixedWidth(width + 160)  # Adjust width as needed
        self.mean5_text.setReadOnly(True)
        self.layout.addWidget(self.mean5_text, 5, 1)
        
        self.std_label = QLabel('Std Dev:', self)
        self.layout.addWidget(self.std_label, 6, 0)
        
        self.std_text = QLineEdit(self)
        self.std_text.setFixedWidth(width)  # Adjust width as needed
        self.std_text.setReadOnly(True)
        self.layout.addWidget(self.std_text, 6, 1)
        
        # 이력 표시
        self.history_label = QLabel('History:', self)
        self.layout.addWidget(self.history_label, 7, 0)
        
        self.history_text = QTextEdit(self)
        self.history_text.setMinimumHeight(height)  # Adjust minimum height as needed
        self.history_text.setMinimumWidth(width_history)  # Adjust minimum width as needed
        self.history_text.setReadOnly(True)
        self.layout.addWidget(self.history_text, 7, 1)
        
    
    def init_data(self): 
        # 초기 설정 로드
        self.load_config()
        
        # 설정 변경은 아직 구현하지 않았습니다.
        
        # 초기 이력 로드
        print(self.config)
        self.load_history((self.config['history_directory'], self.config['default_record']))
        
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
            raise 'No config file found.'
        
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
        
    def load_history(self, record):
        # 이력 로드
        dir = './'.join(record)
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
                        # print("No match")
                        raise ValueError("Invalid cube type found in history.")
                self.history_text.setText('\n'.join(history[-20:]))
                self.record_text.setText(record[-1])
                
                self.timelist = [parse_time(entry.split(' - ')[0]) for entry in history]
                self.timelist = [time for time in self.timelist if time is not None]
        except FileNotFoundError:
            self.history_text.setText('No history found.')
        except ValueError as e:
            self.history_text.setText('Error loading history: ' + str(e))
        
        print('load_history :', self.cube_type)
        
        
        self.statistics_update()
        self.generate_scramble()
            
    def save_history(self, entry, record):
        dir = './'.join(record)
        with open(dir, 'a') as file:
            file.write(entry + '\n')
        self.load_history(record)
        
    def keyPressEvent(self, e): #키가 눌러졌을 때 실행됨
        # space bar is pressed
        if e.key() == Qt.Key_Space:
            self.timer_toggle(on = False)
            return
        if e.key() == Qt.Key_Return:
            self.reset_timer()
            return

    def keyReleaseEvent(self,e): #키를 누른상태에서 뗐을 때 실행됨
        #space bar is released
        if e.key() == Qt.Key_Space and not e.isAutoRepeat():
            self.timer_toggle(on = True)
            return
    
    def timer_toggle(self, on):
        if self.timer_running and not on:
            self.timer_save_button.setEnabled(True)
            self.stop_timer()
            self.save_time()
            return
        if not self.timer_running and on:
            self.timer_save_button.setEnabled(False)
            self.timer_running = True
            self.start_timer()
            return
        if self.timer_running and on:
            self.timer_running = False
            return
        
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
            (self.config['history_directory'], self.config['default_record'])
        )
    
    def select_record(self):
        self.child_window = SelectRecordDialog(self, self.config['history_directory'])
        self.child_window.data_sent.connect(self.handle_data)  # 시그널 연결
        self.child_window.show()
    
    def handle_data(self, record):
        self.load_history((self.config['history_directory'], record))
        self.child_window.close()
        
    def statistics_update(self):
        # 통계 업데이트
        if (len(self.timelist) == 0):
            self.mean_text.setText("00:00:000")
            self.mean5_text.setText("00:00:000")
            self.std_text.setText("00:00:000")
            return
        mean = stat.mean(self.timelist)
        mean = format_time(mean)
        std = 0 if len(self.timelist) == 1 else stat.stdev(self.timelist)
        std = format_time(std)
        # print(timelist)
        # print(mean, std)
        self.mean_text.setText(mean)
        self.mean5_text.setText(format_time(stat.mean(self.timelist[-5:])))
        self.std_text.setText(std)
