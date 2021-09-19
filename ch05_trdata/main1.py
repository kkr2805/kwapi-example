import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QAxContainer import QAxWidget

def do_request_kwtr_daily_price(code, yyyymmdd):
    kw_api.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
    kw_api.dynamicCall("SetInputValue(QString, QString)", "조회일자", yyyymmdd)
    kw_api.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10086_req", "opt10086", 0, "1051")

def event_connect(err_code):
    if err_code == 0:
        print("로그인 성공")
        do_request_kwtr_daily_price("005930", "20210912")
    elif err_code == 100:
        print("사용자 정보교환 실패")
    elif err_code == 101:
        print("서버접속 실패")
    elif err_code == 102:
        print("버전처리 실패")

def receive_trdata(screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
    if rqname == "opt10086_req":
        count = kw_api.dynamicCall("GetRepeatCnt(QString, QString)", "opt10086", "opt10086_req")
        for index in range(0, count):
            date = kw_api.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, index, "날짜")
            date = date.strip()
            price = kw_api.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, index, "종가")
            price = price.strip()
            if price.startswith('-') or price.startswith('+'):
                price = price[1:]
            print(date + " : " + price)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.show()
    
    kw_api = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
    ret = kw_api.dynamicCall("CommConnect()")
    kw_api.OnEventConnect.connect(event_connect)
    kw_api.OnReceiveTrData.connect(receive_trdata)

    app.exec_()