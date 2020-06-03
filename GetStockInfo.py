import urllib.parse
import pandas as pd

MARKET_CODE_DICT = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt',
    'konex': 'konexMkt'
}

DOWNLOAD_URL = 'kind.krx.co.kr/corpgeneral/corpList.do'

def download_stock_codes(market=None, delisted=False):
    params = {'method': 'download'}

    if market.lower() in MARKET_CODE_DICT:
        params['marketType'] = MARKET_CODE_DICT[market]

    if not delisted:
        params['searchType'] = 13

    params_string = urllib.parse.urlencode(params)
    request_url = urllib.parse.urlunsplit(['http', DOWNLOAD_URL, '', params_string, ''])

    df = pd.read_html(request_url, header=0)[0]
    df.종목코드 = df.종목코드.map('{:06d}'.format)

    return df

if __name__ == "__main__":
    print(1)
    kosdaq_stocks = download_stock_codes('kosdaq')
    kosdaq_stocks.head()

    kospi_stocks = download_stock_codes('kospi')
    kospi_stocks.head()

    konex_stocks = download_stock_codes('konex')
    konex_stocks.head()

    # kosdaq_stocks.to_excel('./test.xlsx')
    # kospi_stocks.to_excel('./test2.xlsx')
    # konex_stocks.to_excel('./test3.xlsx')
    print(kosdaq_stocks)
    print(kospi_stocks)
    print(konex_stocks)