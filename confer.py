import sys
# sys.path.append("..")
# import login as api

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QUrl
import sqlite3

import numpy as np
import pandas as pd

import plotly.offline as po
import plotly.graph_objs as go
from datetime import datetime


#index
#from ta import *
import talib as ta



# from IPython.display import IFrame

main_ui = uic.loadUiType("Pytrader.ui")[0]
login_ui = uic.loadUiType("login.ui")[0]


#login diagram
# class LogInDialog(QDialog,login_ui):
#     def __init__(self,parent=None):
#         QDialog.__init__(self, parent)
#         #super().__init__()
#         self.setupUi(self)
#         self.id = None
#         self.pw1 = None
#         self.pw2 = None
#         self.login = False;
#         self.login_btn.clicked.connect(self.login_btnClicked)
#
#     def login_btnClicked(self):
#         self.id = self.id_val.text()
#         self.pw1 = self.pw1_val.text()
#         self.pw2 = self.pw2_val.text()
#         api.login(self.id, self.pw1, self.pw2)
#         self.close()



#main window
class MyWindow(QMainWindow, main_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        #api connect
        # api 값
        CLSID1 = '{08E39D09-206D-43D1-AC78-D1AE3635A4E9}'
        #A : api , B : btn
        self.account_A = QAxWidget(CLSID1)
        self.account_A.ReceiveData.connect(self.account_A_receive)
        self.account_B.clicked.connect(self.account_btn_clicked)

        #주식보유
        self.mystock_A = QAxWidget(CLSID1)
        self.mystock_A.ReceiveData.connect(self.mystock_A_receive_mult)
        self.mystock_B.clicked.connect(self.mystock_btn_clicked)

        #주식리스트
        self.stocklist_A = QAxWidget(CLSID1)
        self.stocklist_A.ReceiveData.connect(self.stocklist_A_receive)


        #login account pw setting
        self.login_val = False;
        self.Account = str(self.account_A.dynamicCall("GetAccount(int)", 0))
        self.account_LE.setText(self.Account)
        self.PWcode = self.account_A.dynamicCall("GetEncryptPassword(InputData)", self.pw_LE.text())


        #주식잔고
        column_headers = ['종목코드', '종목명', '보유수량', '매입평균', '현재가', '평가손익', '수익율']
        self.mystock_TB.setColumnCount(len(column_headers))
        self.mystock_TB.setHorizontalHeaderLabels(column_headers)
        self.mystock_TB.resizeColumnsToContents()

        #stock list
        #self.stocklist_TB = QTableWidget()
        self.listCode = False
        column_headers = ['종목명', '등락률', '현재가', '거래량', '거래대금','PER' ,'거래량대비', '체결강도']
        self.stocklist_TB.setColumnCount(len(column_headers))
        self.stocklist_TB.setHorizontalHeaderLabels(column_headers)
        self.stocklist_TB.resizeColumnsToContents()
        #최근 변경 셀
        self.RCrow = 0
        self.RCcol = 0
        self.stocklist_TB.cellClicked.connect(self.stocklist_cellDoubleClick)
        self.stocklist_TB.cellChanged.connect(self.stocklist_cellChange)


        #일봉차트
        self.recentcode = 0
        self.daychart_A = QAxWidget(CLSID1)
        self.daychart_A.ReceiveData.connect(self.daychart_A_receive_mult)

        # 분봉차트
        self.minchart_A = QAxWidget(CLSID1)
        self.minchart_A.ReceiveData.connect(self.minchart_A_receive_mult)
        self.minchart_LE.returnPressed.connect(self.changeminchart)
        self.minsize = 0
        self.mincandle_Data = {'Date': [], 'Open': [], 'High': [], 'Low': [], 'Close': [], 'Vol': []}


    def true_strength_index(self,df, r, s):
        """Calculate True Strength Index (TSI) for given data.
        :param df: pandas.DataFrame
        :param r:
        :param s:
        :return: pandas.DataFrame
        """
        M = pd.Series(df.diff(1))
        aM = abs(M)
        EMA1 = pd.Series(M.ewm(span=r, min_periods=r).mean())
        aEMA1 = pd.Series(aM.ewm(span=r, min_periods=r).mean())
        EMA2 = pd.Series(EMA1.ewm(span=s, min_periods=s).mean())
        aEMA2 = pd.Series(aEMA1.ewm(span=s, min_periods=s).mean())
        TSI = pd.Series(EMA2 / aEMA2, name='TSI_' + str(r) + '_' + str(s))
        # df = df.join(TSI)
        # return df
        return TSI

    def stocklist_cellDoubleClick(self,row,col):
        if (self.stocklist_TB.item(row, col) is None):
            return
        if (len(self.stocklist_TB.item(row, col).text()) is 0):
            return
        self.RCrow = row
        self.RCcol = col

        con = sqlite3.connect("c:/Users/kdy/stock.db")
        cursor = con.cursor()
        stockcode = []
        cursor.execute("SELECT * FROM Kosdaq_info WHERE Name = ?;", [self.stocklist_TB.item(row, col).text()])
        stockcode = cursor.fetchall()
        if (len(stockcode) is 0):
            cursor.execute("SELECT * FROM Kospi_info WHERE Name = ?;", [self.stocklist_TB.item(row, col).text()])
            stockcode = cursor.fetchall()
            if (len(stockcode) is 0):
                cursor.execute("SELECT * FROM Konex_info WHERE Name = ?;", [self.stocklist_TB.item(row, col).text()])
                stockcode = cursor.fetchall()

        if(len(stockcode) is not 0):
            self.recentcode = stockcode[0][1]
            self.daychart_A.dynamicCall("SetSingleDataEx(int,int, InputData)", 0, 0, "J")
            self.daychart_A.dynamicCall("SetSingleDataEx(int,int, InputData)", 0, 1, stockcode[0][1])
            self.daychart_A.dynamicCall("SetSingleDataEx(int,int, InputData)",1, 0, "J")
            self.daychart_A.dynamicCall("SetSingleDataEx(int,int, InputData)",1, 1, stockcode[0][1])
            self.daychart_A.dynamicCall("RequestData(QString)", "KST03010100")

            self.minsize = 0
            self.mincandle_Data = {'Date': [], 'Open': [], 'High': [], 'Low': [], 'Close': [], 'Vol': []}
            self.minchart_A.dynamicCall("SetSingleData(int, InputData)", 0, "J")
            self.minchart_A.dynamicCall("SetSingleData(int, InputData)", 1, stockcode[0][1])
            self.minchart_A.dynamicCall("SetSingleData(int, InputData)", 2, str(int(self.minchart_LE.text()) * 60))
            self.minchart_A.dynamicCall("SetSingleData(int, InputData)", 3 ,'Y')
            self.minchart_A.dynamicCall("RequestData(QString)", "PST01010300")

    def changeminchart(self):
        if(self.minchart_LE.text().isdecimal()):
            self.minsize = 0
            self.mincandle_Data = {'Date': [], 'Open': [], 'High': [], 'Low': [], 'Close': [], 'Vol': []}
            self.minchart_A.dynamicCall("SetSingleData(int, InputData)", 0, "J")
            self.minchart_A.dynamicCall("SetSingleData(int, InputData)", 1, self.recentcode)
            self.minchart_A.dynamicCall("SetSingleData(int, InputData)", 2, str(int(self.minchart_LE.text()) * 60))
            self.minchart_A.dynamicCall("SetSingleData(int, InputData)", 3, 'Y')
            self.minchart_A.dynamicCall("RequestData(QString)", "PST01010300")

    def get_html(self, fig):
        raw_html = '<html><head><meta charset="utf-8" />'
        raw_html += '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head>'
        raw_html += '<body>'
        raw_html += po.plot(fig, include_plotlyjs=False, output_type='div')
        raw_html += '</body></html>'
        # setHtml has a 2MB size limit, need to switch to setUrl on tmp file
        # for large figures.
        self.chart1_1.setHtml(raw_html)
        self.chart1_1.show()
        self.chart1_1.raise_()
        return self.chart1_1

    def get_html2(self, fig):
        raw_html = '<html><head><meta charset="utf-8" />'
        raw_html += '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head>'
        raw_html += '<body>'
        raw_html += po.plot(fig, include_plotlyjs=False, output_type='div')
        raw_html += '</body></html>'
        # setHtml has a 2MB size limit, need to switch to setUrl on tmp file
        # for large figures.
        self.chart1_2.setHtml(raw_html)
        self.chart1_2.show()
        self.chart1_2.raise_()
        return self.chart1_2

    def minchart_A_receive_mult(self):
        self.minsize += 1
        if (self.minsize < 15):
            blk = 0
            nRecCount = self.minchart_A.dynamicCall("GetMultiRecordCount(int)", blk)
            for j in range(nRecCount):
                idx = j
                date = self.minchart_A.dynamicCall("GetMultiData(int,int,int,int)", blk, idx, 0, 0)
                hour = self.minchart_A.dynamicCall("GetMultiData(int,int,int,int)", blk, idx, 1, 0)
                self.mincandle_Data['Date'].append(date[0:4] + '-' + date[4:6] + '-' + date[6:8] + '::' + hour[0:2] + ':' + hour[2:4])
                self.mincandle_Data['Open'].append(self.minchart_A.dynamicCall("GetMultiData(int,int,int,int)", blk, idx, 3, 0))
                self.mincandle_Data['High'].append(self.minchart_A.dynamicCall("GetMultiData(int,int,int,int)", blk, idx, 4, 0))
                self.mincandle_Data['Low'].append(self.minchart_A.dynamicCall("GetMultiData(int,int,int,int)", blk, idx, 5, 0))
                self.mincandle_Data['Close'].append(self.minchart_A.dynamicCall("GetMultiData(int,int,int,int)", blk, idx, 2, 0))
                self.mincandle_Data['Vol'].append(self.minchart_A.dynamicCall("GetMultiData(int,int,int,int)", blk, idx, 7, 0))
            print(self.minsize)
            self.minchart_A.dynamicCall("RequestNextData()")
        else:
            df = pd.DataFrame(self.mincandle_Data)
            print(df)
            df = df[::-1]
            df['Open'] = pd.to_numeric(df['Open'])
            df['High'] = pd.to_numeric(df['High'])
            df['Close'] = pd.to_numeric(df['Close'])
            df['Low'] = pd.to_numeric(df['Low'])
            df['Vol'] = pd.to_numeric(df['Vol'])

            """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                        chart indicator 생성

            """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            df['MA5'] = ta.SMA(df['Close'], timeperiod=5)
            df['MA20'] = ta.SMA(df['Close'], timeperiod=20)
            df['MA60'] = ta.SMA(df['Close'], timeperiod=60)
            df['MA120'] = ta.SMA(df['Close'], timeperiod=120)

            adx_period = 26
            df['ADX'] = ta.ADX(df['High'], df['Low'], df['Close'], timeperiod=adx_period)
            df['PDI'] = ta.PLUS_DI(df['High'], df['Low'], df['Close'], timeperiod=adx_period)
            df['MDI'] = ta.MINUS_DI(df['High'], df['Low'], df['Close'], timeperiod=adx_period)
            # fastk, fastd = ta.STOCHRSI(df['Close'], timeperiod=14, fastk_period=3, fastd_period=3, fastd_matype=0)
            # df['stofastk'] = fastk
            # df['stofastd'] = fastd
            df['OBV'] = ta.OBV(df['Close'], df['Vol'])
            rsi_period = 13
            df['RSI'] = ta.RSI(df['Close'], timeperiod=rsi_period)
            rsi_signal = 13
            RSI_S = df['RSI'].rolling(window=rsi_signal).mean()
            df.insert(len(df.columns), "RSI_S", RSI_S)
            try:
                df['TSI'] = self.true_strength_index(df['Close'], r=20, s=7)
            except Exception as ex:
                print(ex)
            """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                chart range 1/4 생성

            """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            max_p = df['High'].max()
            min_p = df['Low'].min()
            p4_1 = min_p
            p4_2 = p4_1 + ((max_p - min_p) / 4)
            p4_3 = (min_p + max_p) / 2
            p4_4 = p4_3 + ((max_p - min_p) / 4)
            p4_5 = max_p

            trace = go.Candlestick(
                # x=dates ,
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing=dict(line=dict(color='#FA5858')),
                decreasing=dict(line=dict(color='#58ACFA'))
            )

            ma5 = go.Scatter(
                x=df['Date'],
                y=df['MA5'],
                mode='lines',
                name='ma5',
                line=dict(
                    color=('rgb(255, 0, 0)'),
                    width=1)
            )
            ma20 = go.Scatter(
                x=df['Date'],
                y=df['MA20'],
                mode='lines',
                name='ma20',
                line=dict(
                    color=('rgb(0, 0, 0)'),
                    width=1)
            )
            ma60 = go.Scatter(
                x=df['Date'],
                y=df['MA60'],
                mode='lines',
                name='ma60',
                line=dict(
                    color=('rgb(0, 0, 120)'),
                    width=1)
            )

            ma120 = go.Scatter(
                x=df['Date'],
                y=df['MA120'],
                mode='lines',
                name='ma60',
                line=dict(
                    color=('rgb(0, 255, 0)'),
                    width=1)
            )

            ADX_adx = go.Scatter(
                x=df['Date'],
                y=df['ADX'],
                mode='lines',
                name='adx',
                line=dict(
                    color=('rgb(0, 0, 0)'),
                    width=2),
                yaxis="y2"
            )
            ADX_pdi = go.Scatter(
                x=df['Date'],
                y=df['PDI'],
                mode='lines',
                name='PDI',
                line=dict(
                    color=('rgb(255, 0, 0)'),
                    width=2),
                yaxis="y2"
            )
            ADX_mdi = go.Scatter(
                x=df['Date'],
                y=df['MDI'],
                mode='lines',
                name='MDI',
                line=dict(
                    color=('rgb(0, 0, 255)'),
                    width=2),
                yaxis="y2"
            )

            RSI = go.Scatter(
                x=df['Date'],
                y=df['RSI'],
                mode='lines',
                name='RSI',
                line=dict(
                    color=('rgb(255, 120, 0)'),
                    width=1),
                yaxis="y3"
            )

            RSI_S = go.Scatter(
                x=df['Date'],
                y=df['RSI_S'],
                mode='lines',
                name='RSI',
                line=dict(
                    color=('rgb(0, 120, 120)'),
                    width=1),
                yaxis="y3"
            )

            TSI = go.Scatter(
                x=df['Date'],
                y=df['TSI'],
                mode='lines',
                name='TSI',
                line=dict(
                    color=('rgb(200, 120, 120)'),
                    width=1),
                yaxis="y4"
            )

            # STORSI_K = go.Scatter(
            #     x=df['Date'],
            #     y=df['stofastk'],
            #     mode='lines',
            #     name='stofastk',
            #     line=dict(
            #         color=('rgb(200, 120, 120)'),
            #         width=1),
            #     yaxis="y5"
            # )
            # STORSI_D = go.Scatter(
            #     x=df['Date'],
            #     y=df['stofastd'],
            #     mode='lines',
            #     name='stofastd',
            #     line=dict(
            #         color=('rgb(120, 120, 200)'),
            #         width=1),
            #     yaxis="y5"
            # )

            OBV = go.Scatter(
                x=df['Date'],
                y=df['OBV'],
                mode='lines',
                name='OBV',
                line=dict(
                    color=('rgb(120, 120, 200)'),
                    width=1),
                yaxis="y5"
            )

            data = [trace, ma5, ma20, ma60, ma120, ADX_adx, ADX_pdi, ADX_mdi, RSI, RSI_S, TSI, OBV]

            layout = go.Layout(
                margin=go.layout.Margin(
                    l=40,
                    r=0,
                    b=0,
                    t=0,
                    pad=0
                ),
                xaxis=dict(
                    domain=[0, 1],
                    rangeslider=dict(
                        visible=False
                    ),
                    showline=True,
                    showticklabels=False,
                    type='category'
                ),

                yaxis=dict(
                    scaleanchor="x",
                    domain=[0.6, 1],

                    # tickmode='linear',
                    # ticks='outside',
                    # showticklabels=True,
                    # tickfont=dict(
                    #     family='Old Standard TT, serif',
                    #     size=14,
                    #     color='black'
                    # ),

                    showline=True
                ),
                # adx
                yaxis2=dict(
                    scaleanchor="x",
                    range=[5, 60],
                    domain=[0.45, 0.6],
                    showline=True
                ),
                # rsi
                yaxis3=dict(
                    scaleanchor="x",
                    range=[10, 100],
                    domain=[0.3, 0.45],
                    showline=True
                ),
                yaxis4=dict(
                    scaleanchor="x",
                    # range=[10, 100],
                    domain=[0.15, 0.3],
                    showline=True
                ),
                yaxis5=dict(
                    scaleanchor="x",
                    # range=[10, 100],
                    domain=[0.07, 0.15],
                    showline=True
                ),
                shapes=[
                    dict(
                        type='line',
                        xref='x1',
                        yref='y3',
                        x0=df['Date'][0],
                        x1=df['Date'][len(df['Date']) - 1],
                        y0=80,
                        y1=80,
                        line=dict(
                            color=('rgb(255, 120, 0)'),
                            width=1
                        )
                    ),
                    dict(
                        type='line',
                        xref='x1',
                        yref='y3',
                        x0=df['Date'][0],
                        x1=df['Date'][len(df['Date']) - 1],
                        y0=20,
                        y1=20,
                        line=dict(
                            color=('rgb(255, 120, 0)'),
                            width=1
                        )
                    ),
                    dict(
                        type='line',
                        xref='x1',
                        yref='y3',
                        x0=df['Date'][0],
                        x1=df['Date'][len(df['Date']) - 1],
                        y0=10,
                        y1=10,
                        line=dict(
                            color=('rgb(0, 0, 0)'),
                            width=2
                        )
                    ),
                    dict(
                        type='line',
                        xref='x1',
                        yref='y3',
                        x0=df['Date'][0],
                        x1=df['Date'][len(df['Date']) - 1],
                        y0=100,
                        y1=100,
                        line=dict(
                            color=('rgb(0, 0, 0)'),
                            width=2
                        )
                    ),
                    dict(
                        type='line',
                        xref='x1',
                        yref='y2',
                        x0=df['Date'][0],
                        x1=df['Date'][len(df['Date']) - 1],
                        y0=60,
                        y1=60,
                        line=dict(
                            color=('rgb(0, 0, 0)'),
                            width=2
                        )
                    ),

                    # 1/4선
                    dict(
                        type='line',
                        xref='x1',
                        yref='y1',
                        x0=df['Date'][0],
                        x1=df['Date'][len(df['Date']) - 1],
                        y0=p4_1,
                        y1=p4_1,
                        line=dict(
                            color=('rgb(0, 0, 0)'),
                            width=1
                        )
                    ),
                    dict(
                        type='line',
                        xref='x1',
                        yref='y1',
                        x0=df['Date'][0],
                        x1=df['Date'][len(df['Date']) - 1],
                        y0=p4_2,
                        y1=p4_2,
                        line=dict(
                            color=('rgb(0, 0, 0)'),
                            width=1
                        )
                    ),
                    dict(
                        type='line',
                        xref='x1',
                        yref='y1',
                        x0=df['Date'][0],
                        x1=df['Date'][len(df['Date']) - 1],
                        y0=p4_3,
                        y1=p4_3,
                        line=dict(
                            color=('rgb(0, 0, 0)'),
                            width=1
                        )
                    ),
                    dict(
                        type='line',
                        xref='x1',
                        yref='y1',
                        x0=df['Date'][0],
                        x1=df['Date'][len(df['Date']) - 1],
                        y0=p4_4,
                        y1=p4_4,
                        line=dict(
                            color=('rgb(0, 0, 0)'),
                            width=1
                        )
                    ),
                    dict(
                        type='line',
                        xref='x1',
                        yref='y1',
                        x0=df['Date'][0],
                        x1=df['Date'][len(df['Date']) - 1],
                        y0=p4_5,
                        y1=p4_5,
                        line=dict(
                            color=('rgb(0, 0, 0)'),
                            width=1
                        )
                    )
                ],

                showlegend=False
            )

            fig = go.Figure(data=data, layout=layout)
            # raw_html = self.show_qt(fig)
            self.chart1_2 = self.get_html2(fig)


    def daychart_A_receive_mult(self):
        error_code = self.daychart_A.dynamicCall("GetReqMsgCode()")
        error_message = self.daychart_A.dynamicCall("GetReqMessage()")
        self.error_L.setText(error_code + "  " + error_message)

        candle_Data ={'Date': [], 'Open':[],'High':[],'Low':[],'Close':[], 'Vol':[]}
        #candle_Data = { 'Open': [], 'High': [], 'Low': [], 'Close': [], 'Vol': []}
        #dates =[]
        blk = 1
        nRecCount = self.daychart_A.dynamicCall("GetMultiRecordCount(int)", blk)
        # print(nRecCount)
        for j in range(nRecCount):
            idx = nRecCount - 1 - j
            date = self.daychart_A.dynamicCall("GetMultiData(int,int,int,int)", blk, idx, 0, 0)
            #val = datetime(year=int(date[0:4]), month=int(date[4:6]), day=int(date[6:8])),
            candle_Data['Date'].append(date[0:4]+'-'+date[4:6]+'-'+date[6:8])
            #dates.append(val)
            candle_Data['Open'].append(self.daychart_A.dynamicCall("GetMultiData(int,int,int,int)", blk, idx, 2, 0))
            candle_Data['High'].append(self.daychart_A.dynamicCall("GetMultiData(int,int,int,int)", blk, idx, 3, 0))
            candle_Data['Low'].append(self.daychart_A.dynamicCall("GetMultiData(int,int,int,int)", blk, idx, 4, 0))
            candle_Data['Close'].append(self.daychart_A.dynamicCall("GetMultiData(int,int,int,int)", blk, idx, 1, 0))
            candle_Data['Vol'].append(self.daychart_A.dynamicCall("GetMultiData(int,int,int,int)", blk, idx, 5, 0))
        df = pd.DataFrame(candle_Data)

        df['Open'] = pd.to_numeric(df['Open'])
        df['High'] = pd.to_numeric(df['High'])
        df['Close'] = pd.to_numeric(df['Close'])
        df['Low'] = pd.to_numeric(df['Low'])
        df['Vol'] = pd.to_numeric(df['Vol'])

        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            chart indicator 생성
            
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        #real = ta.ADX(df['High'], df['Low'], df['Close'], timeperiod=14)

        df['MA5'] = ta.SMA(df['Close'], timeperiod=5)
        df['MA20'] = ta.SMA(df['Close'], timeperiod=20)
        df['MA60'] = ta.SMA(df['Close'], timeperiod=60)
        df['MA120'] = ta.SMA(df['Close'], timeperiod=120)

        adx_period = 26
        df['ADX'] = ta.ADX(df['High'], df['Low'], df['Close'], timeperiod=adx_period)
        df['PDI'] = ta.PLUS_DI(df['High'], df['Low'], df['Close'], timeperiod=adx_period)
        df['MDI'] = ta.MINUS_DI(df['High'], df['Low'], df['Close'], timeperiod=adx_period)

        #fastk, fastd = ta.STOCHRSI(df['Close'], timeperiod=14, fastk_period=3, fastd_period=3, fastd_matype=0)
        # df['stofastk'] = fastk
        # df['stofastd'] = fastd
        df['OBV'] = ta.OBV(df['Close'], df['Vol'])


        rsi_period = 13
        df['RSI'] = ta.RSI(df['Close'], timeperiod=rsi_period)
        rsi_signal = 13
        RSI_S = df['RSI'].rolling(window=rsi_signal).mean()
        df.insert(len(df.columns), "RSI_S", RSI_S)

        try:
            df['TSI'] = self.true_strength_index(df['Close'], r=20, s=7)
        except Exception as ex:
            print(ex)

        # df['TSI'] = true_strength_index(df['Close'], r=25, s=13)

        # df['ma20'] = ta.SMA(np.asarray(df['close']), 20)
        # df['ma60'] = ta.SMA(np.asarray(df['close']), 60)
        # df['ma120'] = ta.SMA(np.asarray(df['close']), 120)
        # ma5 = df['Close'].rolling(window=5).mean()
        # df.insert(len(df.columns),"MA5",ma5)
        # ma20 = df['Close'].rolling(window=20).mean()
        # df.insert(len(df.columns), "MA20", ma20)
        # ma60 = df['Close'].rolling(window=60).mean()
        # df.insert(len(df.columns), "MA60", ma60)
        # ma120 = df['Close'].rolling(window=120).mean()
        # df.insert(len(df.columns), "MA120", ma120)

        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    chart range 1/4 생성

        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # mask = (df['Date'] > '2018-6-1') & (df['Date'] <= '2019-5-10')
        # print(df.loc[mask])
        # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        # df = df.set_index(['date'])
        # print(df.loc['2019-1-2':'2019-3-10'])
        max_p = df['High'].max()
        min_p = df['Low'].min()

        p4_1 = min_p
        p4_2 = p4_1 + ((max_p - min_p) / 4)
        p4_3 = (min_p + max_p) / 2
        p4_4 = p4_3 + ((max_p - min_p) / 4)
        p4_5 = max_p


        #print(dates)
        #df.to_csv("./test.csv")
        # df.to_excel("./test.xlsx")

        trace = go.Candlestick(
            #x=dates ,
            x= df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            increasing=dict(line=dict(color='#FA5858')),
            decreasing=dict(line=dict(color='#58ACFA'))
        )

        ma5 = go.Scatter(
            x=df['Date'],
            y=df['MA5'],
            mode='lines',
            name='ma5',
            line = dict(
            color=('rgb(255, 0, 0)'),
            width=1 )
        )
        ma20 = go.Scatter(
            x=df['Date'],
            y=df['MA20'],
            mode='lines',
            name='ma20',
            line=dict(
                color=('rgb(0, 0, 0)'),
                width=1)
        )
        ma60 = go.Scatter(
            x=df['Date'],
            y=df['MA60'],
            mode='lines',
            name='ma60',
            line=dict(
                color=('rgb(0, 0, 120)'),
                width=1)
        )

        ma120 = go.Scatter(
            x=df['Date'],
            y=df['MA120'],
            mode='lines',
            name='ma60',
            line=dict(
                color=('rgb(0, 255, 0)'),
                width=1)
        )


        ADX_adx = go.Scatter(
            x=df['Date'],
            y=df['ADX'],
            mode='lines',
            name='adx',
            line=dict(
                color=('rgb(0, 0, 0)'),
                width=2),
            yaxis="y2"
        )
        ADX_pdi = go.Scatter(
            x=df['Date'],
            y=df['PDI'],
            mode='lines',
            name='PDI',
            line=dict(
                color=('rgb(255, 0, 0)'),
                width=2),
            yaxis="y2"
        )
        ADX_mdi = go.Scatter(
            x=df['Date'],
            y=df['MDI'],
            mode='lines',
            name='MDI',
            line=dict(
                color=('rgb(0, 0, 255)'),
                width=2),
            yaxis="y2"
        )

        RSI = go.Scatter(
            x=df['Date'],
            y=df['RSI'],
            mode='lines',
            name='RSI',
            line=dict(
                color=('rgb(255, 120, 0)'),
                width=1),
            yaxis="y3"
        )

        RSI_S = go.Scatter(
            x=df['Date'],
            y=df['RSI_S'],
            mode='lines',
            name='RSI',
            line=dict(
                color=('rgb(0, 120, 120)'),
                width=1),
            yaxis="y3"
        )

        TSI = go.Scatter(
            x=df['Date'],
            y=df['TSI'],
            mode='lines',
            name='TSI',
            line=dict(
                color=('rgb(200, 120, 120)'),
                width=1),
            yaxis="y4"
        )

        # STORSI_K = go.Scatter(
        #     x=df['Date'],
        #     y=df['stofastk'],
        #     mode='lines',
        #     name='stofastk',
        #     line=dict(
        #         color=('rgb(200, 120, 120)'),
        #         width=1),
        #     yaxis="y5"
        # )
        # STORSI_D = go.Scatter(
        #     x=df['Date'],
        #     y=df['stofastd'],
        #     mode='lines',
        #     name='stofastd',
        #     line=dict(
        #         color=('rgb(120, 120, 200)'),
        #         width=1),
        #     yaxis="y5"
        # )

        OBV = go.Scatter(
            x=df['Date'],
            y=df['OBV'],
            mode='lines',
            name='OBV',
            line=dict(
                color=('rgb(120, 120, 200)'),
                width=1),
            yaxis="y5"
        )

        data = [trace,ma5,ma20,ma60,ma120,ADX_adx,ADX_pdi,ADX_mdi,RSI,RSI_S,TSI,OBV]
        layout = go.Layout(
            margin=go.layout.Margin(
                l=40,
                r=0,
                b=0,
                t=0,
                pad=0
            ),
            xaxis=dict(
                domain=[0, 1],
                rangeslider=dict(
                    visible=False
                ),
                showline = True,
                showticklabels=False,
                type = 'category'
            ),

            yaxis=dict(
                scaleanchor="x",
                domain=[0.6, 1],

                # tickmode='linear',
                # ticks='outside',
                # showticklabels=True,
                # tickfont=dict(
                #     family='Old Standard TT, serif',
                #     size=14,
                #     color='black'
                # ),

                showline=True
            ),
            #adx
            yaxis2=dict(
                scaleanchor="x",
                range=[5, 60],
                domain=[0.45, 0.6],
                showline=True
            ),
            #rsi
            yaxis3=dict(
                scaleanchor="x",
                range=[10, 100],
                domain=[0.3, 0.45],
                showline=True
            ),
            yaxis4=dict(
                scaleanchor="x",
                #range=[10, 100],
                domain=[0.15, 0.3],
                showline=True
            ),
            yaxis5=dict(
                scaleanchor="x",
                # range=[10, 100],
                domain=[0.07, 0.15],
                showline=True
            ),
            shapes=[
                dict(
                    type='line',
                    xref='x1',
                    yref='y3',
                    x0=df['Date'][0],
                    x1=df['Date'][len(df['Date']) - 1],
                    y0=80,
                    y1=80,
                    line=dict(
                        color=('rgb(255, 120, 0)'),
                        width=1
                    )
                ),
                dict(
                    type='line',
                    xref='x1',
                    yref='y3',
                    x0=df['Date'][0],
                    x1=df['Date'][len(df['Date']) - 1],
                    y0=20,
                    y1=20,
                    line=dict(
                        color=('rgb(255, 120, 0)'),
                        width=1
                    )
                ),
                dict(
                    type='line',
                    xref='x1',
                    yref='y3',
                    x0=df['Date'][0],
                    x1=df['Date'][len(df['Date']) - 1],
                    y0=10,
                    y1=10,
                    line=dict(
                        color=('rgb(0, 0, 0)'),
                        width=2
                    )
                ),
                dict(
                    type='line',
                    xref='x1',
                    yref='y3',
                    x0=df['Date'][0],
                    x1=df['Date'][len(df['Date']) - 1],
                    y0=100,
                    y1=100,
                    line=dict(
                        color=('rgb(0, 0, 0)'),
                        width=2
                    )
                ),
                dict(
                    type='line',
                    xref='x1',
                    yref='y2',
                    x0=df['Date'][0],
                    x1=df['Date'][len(df['Date']) - 1],
                    y0=60,
                    y1=60,
                    line=dict(
                        color=('rgb(0, 0, 0)'),
                        width=2
                    )
                ),

                #1/4선
                dict(
                    type='line',
                    xref='x1',
                    yref='y1',
                    x0=df['Date'][0],
                    x1=df['Date'][len(df['Date']) - 1],
                    y0=p4_1,
                    y1=p4_1,
                    line=dict(
                        color=('rgb(0, 0, 0)'),
                        width=1
                    )
                ),
                dict(
                    type='line',
                    xref='x1',
                    yref='y1',
                    x0=df['Date'][0],
                    x1=df['Date'][len(df['Date']) - 1],
                    y0=p4_2,
                    y1=p4_2,
                    line=dict(
                        color=('rgb(0, 0, 0)'),
                        width=1
                    )
                ),
                dict(
                    type='line',
                    xref='x1',
                    yref='y1',
                    x0=df['Date'][0],
                    x1=df['Date'][len(df['Date']) - 1],
                    y0=p4_3,
                    y1=p4_3,
                    line=dict(
                        color=('rgb(0, 0, 0)'),
                        width=1
                    )
                ),
                dict(
                    type='line',
                    xref='x1',
                    yref='y1',
                    x0=df['Date'][0],
                    x1=df['Date'][len(df['Date']) - 1],
                    y0=p4_4,
                    y1=p4_4,
                    line=dict(
                        color=('rgb(0, 0, 0)'),
                        width=1
                    )
                ),
                dict(
                    type='line',
                    xref='x1',
                    yref='y1',
                    x0=df['Date'][0],
                    x1=df['Date'][len(df['Date']) - 1],
                    y0=p4_5,
                    y1=p4_5,
                    line=dict(
                        color=('rgb(0, 0, 0)'),
                        width=1
                    )
                )
            ],

            showlegend=False
        )


        fig = go.Figure(data=data, layout=layout)
        #raw_html = self.show_qt(fig)
        self.chart1_1 = self.get_html(fig)


    def stocklist_cellChange(self, row, col):
        if(self.listCode):
            return
        if (col is not 0 ):
            # temp = QTableWidget()
            # temp.clearContents()
            return

        self.RCrow = row
        self.RCcol = col

        con = sqlite3.connect("c:/Users/kdy/stock.db")
        cursor = con.cursor()
        stockcode = []
        cursor.execute("SELECT * FROM Kosdaq_info WHERE Name = ?;", [self.stocklist_TB.item(row,col).text()])
        stockcode = cursor.fetchall()
        if(len(stockcode) is 0):
            cursor.execute("SELECT * FROM Kospi_info WHERE Name = ?;", [self.stocklist_TB.item(row,col).text()])
            stockcode = cursor.fetchall()
            if(len(stockcode) is 0):
                cursor.execute("SELECT * FROM Konex_info WHERE Name = ?;", [self.stocklist_TB.item(row,col).text()])
                stockcode = cursor.fetchall()

        #찾을수 없음 ->code로
        if(len(stockcode) is 0):
            cursor.execute("SELECT * FROM Kosdaq_info WHERE Code = ?;", [self.stocklist_TB.item(row, col).text()])
            stockcode = cursor.fetchall()
            if (len(stockcode) is 0):
                cursor.execute("SELECT * FROM Kospi_info WHERE Code = ?;", [self.stocklist_TB.item(row, col).text()])
                stockcode = cursor.fetchall()
                if (len(stockcode) is 0):
                    cursor.execute("SELECT * FROM Konex_info WHERE Code = ?;",[self.stocklist_TB.item(row, col).text()])
                    stockcode = cursor.fetchall()
            if (len(stockcode) is 0):
                return
            self.listCode =True
            temp = QTableWidgetItem(stockcode[0][0])
            self.stocklist_TB.setItem(self.RCrow, 0, temp)
            self.listCode = False


        self.stocklist_A.dynamicCall("SetSingleData(int, InputData)", 0, "J")
        self.stocklist_A.dynamicCall("SetSingleData(int, InputData)", 1, stockcode[0][1])
        self.stocklist_A.dynamicCall("RequestData(QString)", "SCP")


    def stocklist_A_receive(self):
        error_code = self.stocklist_A.dynamicCall("GetReqMsgCode()")
        error_message = self.stocklist_A.dynamicCall("GetReqMessage()")
        self.error_L.setText(error_code + "  " + error_message)


        #등략률
        MR = self.stocklist_A.dynamicCall("GetSingleData(int,int)", 14, 0)
        #현재가
        PP = self.stocklist_A.dynamicCall("GetSingleData(int,int)", 11, 0)
        PP =format(int(float(PP)), ',')
        #거래대금
        EM = self.stocklist_A.dynamicCall("GetSingleData(int,int)", 15, 0)
        EM = format(int(float(EM)), ',')
        #거래량
        EA = self.stocklist_A.dynamicCall("GetSingleData(int,int)", 16, 0)
        EA = format(int(float(EA)), ',')
        #PER
        PER = self.stocklist_A.dynamicCall("GetSingleData(int,int)", 43, 0)
        list = [MR,PP,EM,EA,PER]

        for i in range(len(list)):
            temp = QTableWidgetItem(list[i])
            temp.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.stocklist_TB.setItem(self.RCrow,i+1,temp)
        self.stocklist_TB.resizeColumnsToContents()
        self.mystock_TB.resizeRowsToContents()

        # self.login_act.triggered.connect(self.login_btn_clicked)
    # def login_btn_clicked(self):
    #     dlg = LogInDialog()
    #     #self.login_L.setText("로그인 완료") #나중에 처리
    #     dlg.exec_()

    def Get_DB_info(Sector):
        con = sqlite3.connect("c:/Users/kdy/stock.db")
        cursor = con.cursor()
        # cursor.execute("SELECT * FROM Konex_info WHERE Name = ?;","유비온")
        cursor.execute("SELECT * FROM " + Sector)
        stock = cursor.fetchall()
        return stock

    def account_btn_clicked(self):
        # count = self.account_A.dynamicCall("GetAccountCount()")
        # for i in range(count):
        #     Account = str(self.kiwoom.dynamicCall("GetAccount(int)", i))
        #     self.account_LE.setText(Account)

        #Brcode = self.account_A.dynamicCall("GetAccountBrcode(InputData)",Account)

        self.account_A.dynamicCall("SetSingleData(int, InputData)", 0, self.Account[:8])
        self.account_A.dynamicCall("SetSingleData(int, InputData)", 1, self.Account[8:])
        self.account_A.dynamicCall("SetSingleData(int, InputData)", 2, self.PWcode)
        self.account_A.dynamicCall("SetSingleData(int, InputData)", 5, "02" )

        self.account_A.dynamicCall("RequestData(QString)", "SCAP")

    def account_A_receive(self):
        error_code = self.account_A.dynamicCall("GetReqMsgCode()")
        error_message = self.account_A.dynamicCall("GetReqMessage()")
        self.error_L.setText(error_code +"  "+ error_message)

        deposit = self.account_A.dynamicCall("GetSingleData(int,int)",0,0)
        MAXorder = self.account_A.dynamicCall("GetSingleData(int,int)",7,0)

        self.deposit_L.setText(format(int(deposit),','))
        self.Morder_L.setText(format(int(MAXorder),','))


    def mystock_btn_clicked(self):
        self.mystock_A.dynamicCall("SetSingleData(int, InputData)", 0, self.Account[:8])
        self.mystock_A.dynamicCall("SetSingleData(int, InputData)", 1, self.Account[8:])
        self.mystock_A.dynamicCall("SetSingleData(int, InputData)", 2, self.PWcode)
        self.mystock_A.dynamicCall("SetSingleData(int, InputData)", 5, "02")
        self.mystock_A.dynamicCall("RequestData(QString)", "SATPS")

    def mystock_A_receive_mult(self):
        error_code = self.mystock_A.dynamicCall("GetReqMsgCode()")
        error_message = self.mystock_A.dynamicCall("GetReqMessage()")
        self.error_L.setText(error_code + "  " + error_message)

        stock_temp = {}
        #블럭1 주식 블럭2 계좌현황
        blk = 0
        stock_size = 0
        nRecCount = self.mystock_A.dynamicCall("GetMultiRecordCount(int)", blk)
        stock_size = nRecCount
        for i in range(nRecCount):
            nFieldCount = self.mystock_A.dynamicCall("GetMultiFieldCount(int,int)", blk, i)
            for k in range(nFieldCount):
                t = self.mystock_A.dynamicCall("GetMultiData(int,int,int,int)", blk, i, k, 0)
                if(i is 0):
                    stock_temp[k] = []
                stock_temp[k].append(self.mystock_A.dynamicCall("GetMultiData(int,int,int,int)", blk, i, k, 0))

        column_idx_lookup = { 0 : '종목코드', 1 : '종목명', 7: '보유수량', 9: '매입평균', 11:'현재가', 13: '평가손익', 14:'수익율'}
        stock_show = {}

        # stock table setting
        self.mystock_TB.setRowCount(stock_size)

        indx = 0
        for ind, tval in column_idx_lookup.items():
            stock_show[indx] = stock_temp[ind]
            indx += 1

        for k, v in stock_show.items():
            for row, val in enumerate(v):
                if(3 <= k and k <= 5):
                    val = format(int(float(val)),',')
                item = QTableWidgetItem(val)
                if not(k == 1 and k == 2) :
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.mystock_TB.setItem(row, k, item)
        self.mystock_TB.resizeColumnsToContents()
        self.mystock_TB.resizeRowsToContents()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
