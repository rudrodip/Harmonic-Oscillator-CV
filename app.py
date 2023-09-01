from PyQt5.QtWidgets import QApplication
import sys
from windows.app_window import AppWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
