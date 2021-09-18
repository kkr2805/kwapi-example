import sys
from datetime import date, timedelta, datetime
import time

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QAxContainer import QAxWidget

code = "005930"
start_date = date(2021, 9, 15)
end_date = date(2018, 1, 1)
day_count = (start_date - end_date).days

def do_request_kwtr_daily_price(code, strdate):
    kw_api.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
    kw_api.dynamicCall("SetInputValue(QString, QString)", "조회일자", strdate.strftime("%Y%m%d"))
    kw_api.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10086_req", "opt10086", 0, "1051")

def event_connect(err_code):
    if err_code == 0:
        print("로그인 성공")        
        do_request_kwtr_daily_price(code, start_date)
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
            strdate = kw_api.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, index, "날짜")
            strdate = strdate.strip()
            price = kw_api.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, index, "종가")
            price = price.strip()
            if price.startswith('-') or price.startswith('+'):
                price = price[1:]
            cur_date = datetime.strptime(strdate, "%Y%m%d").date()
            if cur_date < date(2018, 5, 4):
                price = str(int(int(price) / 50))
            print(strdate + " : " + price)
        last_date = datetime.strptime(strdate, "%Y%m%d").date()
        if last_date > end_date:
            time.sleep(0.2)
            do_request_kwtr_daily_price(code, last_date - timedelta(1))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()
    
    kw_api = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
    ret = kw_api.dynamicCall("CommConnect()")
    kw_api.OnEventConnect.connect(event_connect)
    kw_api.OnReceiveTrData.connect(receive_trdata)

    app.exec_()