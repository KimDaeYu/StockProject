import sys

import pymysql
from DB_setting import *

import GetFinancialStatements as GF
import GetStockInfo as GS




KOSPI = 1
KOSDAQ = 2
KONEX = 4

def Insert_DB_info(sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    """kospi"""
    if (sector % 2 == 1):
        data = []
        kospi_stocks = GS.download_stock_codes('kospi')
        for i in range(len(kospi_stocks)):
            print("KOSPI : [{} / {}]".format(i+1,len(kospi_stocks)))
            data.append(list(kospi_stocks.loc[i].fillna('')))
        cursor.executemany("INSERT INTO Kospi_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
        con.commit()
    """kosdaq"""
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        data = []
        kosdaq_stocks = GS.download_stock_codes('kosdaq')
        for i in range(len(kosdaq_stocks)):
            print("KOSDAQ : [{} / {}]".format(i+1,len(kosdaq_stocks)))
            data.append(list(kosdaq_stocks.loc[i].fillna('')))
        cursor.executemany("INSERT INTO Kosdaq_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
        con.commit()
    
    """konex"""
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        data = []
        konex_stocks = GS.download_stock_codes('konex')
        for i in range(len(konex_stocks)):
            print("KONEX : [{} / {}]".format(i+1,len(konex_stocks)))
            data.append(list(konex_stocks.loc[i].fillna('')))
        cursor.executemany("INSERT INTO Konex_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
        con.commit()
    con.close()

if __name__ == "__main__":
    if(len(sys.argv) == 0):
        print("plese set one argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4")
    elif(len(sys.argv) == 2):
        Insert_DB_info(int(sys.argv[1]))
    else:
        print("plese set one argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4")




