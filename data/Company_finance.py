import sys

import pymysql
from DB_setting import *

import GetFinancialStatements as GF
import GetStockInfo as GS

KOSPI = 1
KOSDAQ = 2
KONEX = 4

execute_size = 100

# Sector Kospi_info, Kosdaq_info, Konex_info
def Get_DB_info(Sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM " + Sector)
    stock = cursor.fetchall()
    return stock

def Insert_DB_Qfinance(sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)

    if(sector % 2 == 1):
        kospi = Get_DB_info("Kospi_info")
        data = []
        for num, i in enumerate(kospi):
            print("KOSPI : [{} / {}] {}".format(num+1, len(kospi), i["Code"]))
            temp = GF.StockFinance(i['Code'])
            temp.D_NetQuarterFinance()
            for j in temp.D_A:
                record = [i['Name'], i['Code'], j]
                record.extend(temp.D_A[j].values())
                if len(record) == 28:
                    data.append(record)
            del(temp)
            if(num % execute_size == execute_size-1):
                cursor.executemany("INSERT INTO Kospi_Qfinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
                data = []
                con.commit()
        cursor.executemany("INSERT INTO Kospi_Qfinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        kosdaq = Get_DB_info("Kosdaq_info")
        data = []
        for num ,i in enumerate(kosdaq):
            print("KOSDAQ : [{} / {}] {}".format(num+1, len(kosdaq), i["Code"]))
            temp = GF.StockFinance(i[1])
            temp.D_NetQuarterFinance()
            for j in temp.D_A:
                record = [i['Name'], i['Code'], j]
                record.extend(temp.D_A[j].values())
                if len(record) == 28:
                    data.append(record)
            del(temp)
            if(num % execute_size == execute_size-1):
                cursor.executemany("INSERT INTO Kosdaq_Qfinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
                data = []
                con.commit()
        cursor.executemany("INSERT INTO Kosdaq_Qfinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        konex = Get_DB_info("Konex_info")
        data = []
        for num ,i in enumerate(konex):
            print("KONEX : [{} / {}] {}".format(num+1, len(konex), i["Code"]))
            temp = GF.StockFinance(i[1])
            temp.D_NetQuarterFinance()
            for j in temp.D_A:
                record = [i['Name'], i['Code'], j]
                record.extend(temp.D_A[j].values())
                if len(record) == 28:
                    data.append(record)
            del(temp)
            if(num % execute_size == execute_size-1):
                cursor.executemany("INSERT INTO Kosdaq_Qfinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
                data = []
                con.commit()
        cursor.execute("INSERT INTO Konex_Qfinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
        con.commit()
    con.close()


def Insert_DB_Afinance(sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)

    if(sector % 2 == 1):
        kospi = Get_DB_info("Kospi_info")
        data = []
        for num ,i in enumerate(kospi):
            print("KOSPI : [{} / {}] {}".format(num+1, len(kospi), i["Code"]))
            temp = GF.StockFinance(i['Code'])
            temp.D_AnnualFinance()
            for j in temp.D_Y:
                record = [i['Name'], i['Code'], j]
                record.extend(temp.D_Y[j].values())
                if len(record) == 28:
                    data.append(record)
            del(temp)
            if(num % execute_size == execute_size-1):
                cursor.executemany("INSERT INTO Kospi_Afinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
                data = []
                con.commit()
        cursor.executemany("INSERT INTO Kospi_Afinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        kosdaq = Get_DB_info("Kosdaq_info")
        data = []
        for num ,i in enumerate(kosdaq):
            print("KOSDAQ : [{} / {}] {}".format(num+1, len(kosdaq), i["Code"]))
            temp = GF.StockFinance(i['Code'])
            temp.D_AnnualFinance()
            for j in temp.D_Y:
                record = [i['Name'], i['Code'], j]
                record.extend(temp.D_Y[j].values())
                if len(record) == 28:
                    data.append(record)
            del(temp)
            if(num % execute_size == execute_size-1):
                cursor.executemany("INSERT INTO Kosdaq_Afinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
                data = []
                con.commit()
        cursor.executemany("INSERT INTO Kosdaq_Afinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        konex = Get_DB_info("Konex_info")
        data = []
        for num ,i in enumerate(konex):
            print("KONEX : [{} / {}] {}".format(num+1, len(konex), i["Code"]))
            temp = GF.StockFinance(i['Code'])
            temp.D_AnnualFinance()
            for j in temp.D_Y:
                record = [i['Name'], i['Code'], j]
                record.extend(temp.D_Y[j].values())
                if len(record) == 28:
                    data.append(record)
            del(temp)
            if(num % execute_size == execute_size-1):
                cursor.executemany("INSERT INTO Konex_Afinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
                data = []
                con.commit()
        cursor.execute("INSERT INTO Konex_Afinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
        con.commit()
    con.close()

if __name__ == "__main__":
    if(len(sys.argv) == 0):
        print("plese set two argument :: Annual(A), Quarter(Q) / kospi -> 1 + kosdaq -> 2 + konex -> 4")
    elif(len(sys.argv) == 3):
        if(sys.argv[1] == 'A' or sys.argv[1] == 'Annual'):
            Insert_DB_Afinance(int(sys.argv[2]))
        if(sys.argv[1] == 'Q' or sys.argv[1] == 'Quarter'):
            Insert_DB_Qfinance(int(sys.argv[2]))
    else:
        print("plese set two argument :: Annual(A), Quarter(Q) / kospi -> 1 + kosdaq -> 2 + konex -> 4")
