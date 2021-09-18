import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QAxContainer import QAxWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.show()

    kw_api = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
    ret = kw_api.dynamicCall("CommConnect()")

    app.exec_()