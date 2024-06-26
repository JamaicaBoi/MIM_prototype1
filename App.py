from PyQt5 import QtCore, QtWidgets
from Mainwindow import MainWindow
from HistoryPage import History_Page
from LoginPage import Login_Page
from qt_material import apply_stylesheet
import sys
import os
import shutil


class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)

class App(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}
        
        login = Login_Page()
        Main_win = MainWindow()
        History = History_Page()

        apply_stylesheet(login,theme="light_blue.xml",css_file='UI/style.qss')
        apply_stylesheet(Main_win,theme="light_blue.xml",css_file='UI/style.qss')
        apply_stylesheet(History,theme="light_blue.xml",css_file='UI/style.qss')

        self.register(login, "Login")
        self.register(Main_win, "Main")
        self.register(History, "History")

        self.goto("Login")

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        widget.gotoSignal.connect(self.goto)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())
        if name == "History":
            self.m_pages[name].Import_Examlist_table()

    def closeEvent(self, event):
        if os.path.exists("Examinated_Label"):
            shutil.rmtree("Examinated_Label")
            print("####################Classify time period ####################")
            print(self.m_pages["Main"].classify_time)
            print("###########################################################")
            print("Sample test: ",len(self.m_pages["Main"].classify_time))
            if any(time >= 5 for time in self.m_pages["Main"].classify_time):
                print("Over 5 sec")
            else:
                print("Complete Testing")
                
            


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = App()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()