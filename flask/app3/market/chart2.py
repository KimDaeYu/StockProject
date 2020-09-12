# 필요한 모듈 import 하기
import plotly.offline as offline
import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as po

import plotly
# import talib as ta

import requests
import time
import pandas as pd
import json 

from bs4 import BeautifulSoup as bs
from datetime import datetime


def serial_market(code = "005930"):
    df = pd.DataFrame()
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code = code)

    for page in range(1, 10):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
    df = df.dropna()
    df.head()

    df = df.rename(columns= {'날짜': 'Date', '종가': 'Close', '전일비': 'Diff', '시가': 'Open', '고가': 'High', '저가': 'Low', '거래량': 'Vol'}) 

    # 데이터의 타입을 int형으로 바꿔줌
    df[['Close', 'Diff', 'Open', 'High', 'Low', 'Vol']] \
     = df[['Close', 'Diff', 'Open', 'High', 'Low', 'Vol']].astype(int)

    # 컬럼명 'date'의 타입을 date로 바꿔줌
    df['Date'] = pd.to_datetime(df['Date'])

    # 일자(date)를 기준으로 오름차순 정렬
    df = df.sort_values(by=['Date'], ascending=True)

    return df

def print_chart(code = "005930"):
    start = time.time() 
    df = serial_market(code)
    print("get df time :", time.time() - start)
    """
    columns= {'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'}
    """
    
    MA5 = df['Close'].rolling(window=5).mean()
    df.insert(len(df.columns), "MA5", MA5)
    MA20 = df['Close'].rolling(window=20).mean()
    df.insert(len(df.columns), "MA20", MA20)
    MA60 = df['Close'].rolling(window=60).mean()
    df.insert(len(df.columns), "MA60", MA60)
    MA120 = df['Close'].rolling(window=120).mean()
    df.insert(len(df.columns), "MA120", MA120)
    
    # df['MA5'] = ta.SMA(df['Close'], timeperiod=5)
    # df['MA20'] = ta.SMA(df['Close'], timeperiod=20)
    # df['MA60'] = ta.SMA(df['Close'], timeperiod=60)
    # df['MA120'] = ta.SMA(df['Close'], timeperiod=120)
    
    # adx_period = 26
    # df['ADX'] = ta.ADX(df['High'], df['Low'], df['Close'], timeperiod=adx_period)
    # df['PDI'] = ta.PLUS_DI(df['High'], df['Low'], df['Close'], timeperiod=adx_period)
    # df['MDI'] = ta.MINUS_DI(df['High'], df['Low'], df['Close'], timeperiod=adx_period)
    # # fastk, fastd = ta.STOCHRSI(df['Close'], timeperiod=14, fastk_period=3, fastd_period=3, fastd_matype=0)
    # # df['stofastk'] = fastk
    # # df['stofastd'] = fastd
    # df['OBV'] = ta.OBV(df['Close'], df['Vol'])
    # rsi_period = 13
    # df['RSI'] = ta.RSI(df['Close'], timeperiod=rsi_period)
    # rsi_signal = 13
    # RSI_S = df['RSI'].rolling(window=rsi_signal).mean()
    # df.insert(len(df.columns), "RSI_S", RSI_S)

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
        name='ma120',
        line=dict(
            color=('rgb(0, 255, 0)'),
            width=1)
    )
    
    data = [ma5, ma20, ma60, ma120,trace]
    # data = [celltrion]
    
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
                    domain=[0, 0.8],

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

                showlegend=False
            )
    
    
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    
    layoutJSON = json.dumps(layout, cls=plotly.utils.PlotlyJSONEncoder)
    # fig = go.Figure(data=data, layout=layout)
    
    # config=dict(displaylogo=False,
    #              modeBarButtonsToRemove=['sendDataToCloud'])
    #po.plot(fig, filename='templates/stock.html',auto_open=False)
    
    return graphJSON, layoutJSON
    # print("get html time :", time.time() - start)
    # # fig.write_html("./templates/chart.html")
    # return

