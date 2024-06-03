from .util import parse_time, format_time
from PyQt5.QtWidgets import \
    QLabel, QComboBox, QWidget, QListWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
import os


class SelectRecordDialog(QWidget):
    data_sent = pyqtSignal(str)
    def __init__(self, parent, directory: str):
        super().__init__(parent)
        self.directory = directory
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Select Record")
        self.resize(400, 600)
        
        # 리스트 위젯
        self.list_widget = QListWidget()
        
        # 새 항목 추가를 위한 입력 필드와 버튼
        self.input_line = QLineEdit(self)
        self.add_button = QPushButton("Add new Record", self)
        self.add_button.clicked.connect(self.add_item)
        
        # 닫기 버튼 추가
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close_window)
        
        self.input_layout = QHBoxLayout()
        self.input_layout.addWidget(self.input_line)
        self.input_layout.addWidget(self.add_button)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(self.input_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        self.ui_select_cube_type()
        self.populate_list()
        
        # 리스트 항목 클릭 이벤트 연결
        self.list_widget.itemClicked.connect(self.item_clicked)
        
        self.show()

    def ui_select_cube_type(self):
        # 큐브 종류 선택
        self.cube_type_label = QLabel('Select Cube Type:', self)
        self.input_layout.addWidget(self.cube_type_label)
        
        self.cube_type_combo = QComboBox(self)
        self.cube_type_combo.addItems(['2x2', '3x3', '4x4', '5x5'])
        self.input_layout.addWidget(self.cube_type_combo)
    
    def populate_list(self):
        files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
        self.list_widget.addItems(files)
            
    def item_clicked(self, item):
        print(item.text())
        self.data_sent.emit(item.text())
        # self.close()
    
    def add_item(self):
        item = self.input_line.text()
        try:
            newitemdir = os.path.join(self.directory, item)
            with open(newitemdir, 'w') as f:
                f.write(self.cube_type_combo.currentText() + '\n')
        except FileExistsError:
            print("File already exists")
        self.list_widget.addItem(item)
        self.input_line.clear()
    
    def close_window(self):
        self.close()