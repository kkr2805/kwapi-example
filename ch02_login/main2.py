import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QAxContainer import QAxWidget

def event_connect(err_code):
    if err_code == 0:
        print("로그인 성공")
    elif err_code == 100:
        print("사용자 정보교환 실패")
    elif err_code == 101:
        print("서버접속 실패")
    elif err_code == 102:
        print("버전처리 실패")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.show()

    kw_api = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
    ret = kw_api.dynamicCall("CommConnect()")
    kw_api.OnEventConnect.connect(event_connect)
    
    app.exec_()