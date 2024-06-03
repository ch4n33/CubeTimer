import sys
from PyQt5.QtWidgets import QApplication
from cubetimer import CubeTimerApp

def main():
    app = QApplication(sys.argv)
    window = CubeTimerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()