import requests
import time
import pandas as pd
 
from bs4 import BeautifulSoup as bs
from datetime import datetime


def serial_market(code = "005930"):
    df = pd.DataFrame()
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code = code)

    for page in range(1, 21):
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



