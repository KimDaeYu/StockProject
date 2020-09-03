# 필요한 모듈 import 하기
import plotly.offline as offline
import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as po

from . import day

import talib as ta

def print_chart(code = "005930"):
    df = day.serial_market(code)
    """
    columns= {'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'}
    """

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
    
    data = [trace, ma5, ma20, ma60, ma120, ADX_adx, ADX_pdi, ADX_mdi, RSI, RSI_S, OBV]
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
                    )
                ],

                showlegend=False
            )

    fig = go.Figure(data=data, layout=layout)
    po.plot(fig, filename='templates/stock.html',auto_open=False)
    # fig.write_html("./templates/chart.html")
    return

