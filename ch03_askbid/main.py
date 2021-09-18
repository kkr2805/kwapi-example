import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QAxContainer import QAxWidget

kwreal_askbid_fids = {
    "호가잔량기준시간": 21,
    "매도10차선호가": 50, "매도10차선잔량": 70,
    "매도9차선호가": 49, "매도9차선잔량": 69,
    "매도8차선호가": 48, "매도8차선잔량": 68,
    "매도7차선호가": 47, "매도7차선잔량": 67,
    "매도6차선호가": 46, "매도6차선잔량": 66,
    "매도5차선호가": 45, "매도5차선잔량": 65,
    "매도4차선호가": 44, "매도4차선잔량": 64,
    "매도3차선호가": 43, "매도3차선잔량": 63,
    "매도2차선호가": 42, "매도2차선잔량": 62,
    "매도1차선호가": 41, "매도1차선잔량": 61,
    "매수1차선호가": 51, "매수1차선잔량": 71,
    "매수2차선호가": 52, "매수2차선잔량": 72,
    "매수3차선호가": 53, "매수3차선잔량": 73,
    "매수4차선호가": 54, "매수4차선잔량": 74,
    "매수5차선호가": 55, "매수5차선잔량": 75,
    "매수6차선호가": 56, "매수6차선잔량": 76,
    "매수7차선호가": 57, "매수7차선잔량": 77,
    "매수8차선호가": 58, "매수8차선잔량": 78,
    "매수9차선호가": 59, "매수9차선잔량": 79,
    "매수10차선호가": 60, "매수10차선잔량": 80,
}

def do_request_kwreal_askbid(code):
    kw_fids = ';'.join([str(value) for value in kwreal_askbid_fids.values()])
    kw_api.dynamicCall("SetRealReg(QString, QString, QString, QString)", "1050", code, kw_fids, "1")

def event_connect(err_code):
    if err_code == 0:
        print("로그인 성공")
        do_request_kwreal_askbid("005930")
    elif err_code == 100:
        print("사용자 정보교환 실패")
    elif err_code == 101:
        print("서버접속 실패")
    elif err_code == 102:
        print("버전처리 실패")

def receive_realdata(code, real_type, realdata):
    if real_type == "주식호가잔량":
        items = []
        for fid in kwreal_askbid_fids.values():
            item_data = kw_api.dynamicCall("GetCommRealData(QString, int)", code, fid)
            item_data = item_data.strip()
            if item_data == "":
                item_data = '0'
            if item_data.startswith('-') or item_data.startswith('+'):
                item_data = item_data[1:]
            if fid == 21:
                now = datetime.now()
                today_date = "{0:s}".format(now.strftime("%Y/%m/%d"))
                item_data = today_date + ' ' + ':'.join([item_data[:-4], item_data[-4:-2], item_data[-2:]])
            items.append(item_data)
        
        print("주식호가잔량," + ",".join(items))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.show()

    kw_api = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
    ret = kw_api.dynamicCall("CommConnect()")
    kw_api.OnEventConnect.connect(event_connect)
    kw_api.OnReceiveRealData.connect(receive_realdata)

    app.exec_()