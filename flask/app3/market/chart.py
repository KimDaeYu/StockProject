# 필요한 모듈 import 하기
import plotly.offline as offline
import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as po

from . import day


def print_chart(code = "005930"):
    df = day.serial_market(code)
    # jupyter notebook 에서 출력
    offline.init_notebook_mode(connected=True)
    trace = go.Scatter(x=df.date, y=df.close, name=code)
    data = [trace]
    # data = [celltrion]
    layout = dict(
                title='{}의 종가(close) Time Series'.format(code),
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1, label='1m', step='month', stepmode='backward'),
                            dict(count=3, label='3m', step='month', stepmode='backward'),
                            dict(count=6, label='6m', step='month', stepmode='backward'),
                            dict(step='all')
                        ])
                    ),
                    rangeslider=dict(),
                    type='date'
                )
            )

    fig = go.Figure(data=data, layout=layout)
    po.plot(fig, filename='templates/stock.html',auto_open=False)
    # fig.write_html("./templates/chart.html")
    return

