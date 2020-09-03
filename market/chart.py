# 필요한 모듈 import 하기
import plotly.offline as offline
import plotly.graph_objs as go

from day import *

df = serial_market()
# jupyter notebook 에서 출력
offline.init_notebook_mode(connected=True)
trace = go.Scatter( x=df.date, y=df.close, name=item_name)
data = [trace]
# data = [celltrion]
layout = dict(
            title='{}의 종가(close) Time Series'.format(item_name),
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
offline.iplot(fig)

