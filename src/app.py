import sys

from PyQt5.QtWidgets import QApplication

from ui import MainWindow

#debug
from debug import  setup_manager

setup_manager()


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()