import sys

import pymysql
from DB_setting import *

import GetFinancialStatements_mp as GF
import GetStockInfo as GS

import asyncio
import time

from multiprocessing import Pool, Manager
KOSPI = 1
KOSDAQ = 2
KONEX = 4

execute_size = 50


manager = Manager()
Global = manager.Namespace()
Global.kospi = 0
Global.kosdaq = 0
Global.konex = 0

# Sector Kospi_info, Kosdaq_info, Konex_info
def Get_DB_info(Sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM " + Sector)
    stock = cursor.fetchall()
    return stock


kospi = Get_DB_info("Kospi_info")
kosdaq = Get_DB_info("Kosdaq_info")

def Insert_DB_Qfinance(sector,start_num):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)

    if(sector % 2 == 1):
        try:
            if(start_num + execute_size < len(kospi)):
                stock = [[kospi[x]["Code"],kospi[x]['Name']] for x in range(start_num,start_num+execute_size)]
            else:
                stock = [[kospi[x]["Code"],kospi[x]['Name']] for x in range(start_num,len(kospi))]
        except Exception as err:
            print(start_num + start_num)
            print(err,start_num,execute_size)
        
        Global.kospi += execute_size
        print("kospi processing... {0:0.2f} %".format((Global.kospi/len(kospi)) * 100))
        data_list = []
        #print(stock)
        
        tasks = [GF.StockFinance(x[0],x[1],data_list) for x in stock]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        
        del tasks
        del loop
        
        data = []
        for num, i in enumerate(data_list):
            #print("KOSPI : {} : [{} / {}] {}".format(start_num, num+1, execute_size, i[1]))
            for j in i[0]:
                record = [i[2], i[1], j]
                record.extend(i[0][j].values())
                if len(record) == 28:
                    data.append(record)
            
        #if(num % execute_size == execute_size-1):
        cursor.executemany("INSERT INTO Kospi_Qfinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
        con.commit()
        del data
        del data_list
        
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        try:
            if(start_num + execute_size < len(kosdaq)):
                stock = [[kosdaq[x]["Code"],kosdaq[x]['Name']] for x in range(start_num,start_num+execute_size)]
            else:
                stock = [[kosdaq[x]["Code"],kosdaq[x]['Name']] for x in range(start_num,len(kosdaq))]
        except Exception as err:
            print(start_num + start_num)
            print(err,start_num,execute_size)
        
        Global.kosdaq += execute_size
        print("kosdaq processing... {0:0.2f} %".format((Global.kosdaq/len(kosdaq)) * 100))
        data_list = []
        #print(stock)
        
        tasks = [GF.StockFinance(x[0],x[1],data_list) for x in stock]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

        del tasks
        del loop
        
        data = []
        for num, i in enumerate(data_list):
            #print("KOSPI : {} : [{} / {}] {}".format(start_num, num+1, execute_size, i[1]))
            for j in i[0]:
                record = [i[2], i[1], j]
                record.extend(i[0][j].values())
                if len(record) == 28:
                    data.append(record)
            
        #if(num % execute_size == execute_size-1):
        cursor.executemany("INSERT INTO Kosdaq_Qfinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
        con.commit()
        del data
        del data_list

    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        try:
            if(start_num + execute_size < len(konex)):
                stock = [[konex[x]["Code"],konex[x]['Name']] for x in range(start_num,start_num+execute_size)]
            else:
                stock = [[konex[x]["Code"],konex[x]['Name']] for x in range(start_num,len(konex))]
        except Exception as err:
            print(start_num + start_num)
            print(err,start_num,execute_size)
        
        Global.konex += execute_size
        print("konex processing... {0:0.2f} %".format((Global.KONEXx/len(konex)) * 100))
        data_list = []
        #print(stock)
        
        tasks = [GF.StockFinance(x[0],x[1],data_list) for x in stock]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

        del tasks
        del loop
        
        data = []
        for num, i in enumerate(data_list):
            #print("KOSPI : {} : [{} / {}] {}".format(start_num, num+1, execute_size, i[1]))
            for j in i[0]:
                record = [i[2], i[1], j]
                record.extend(i[0][j].values())
                if len(record) == 28:
                    data.append(record)
            
        #if(num % execute_size == execute_size-1):
        cursor.executemany("INSERT INTO Konex_Qfinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
        con.commit()
        del data
        del data_list
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


def multiprocess(start,market):
    #print(start,market)
    Insert_DB_Qfinance(market,start)


if __name__ == "__main__":
    start_time = time.time()
    pool = Pool(processes=4) #4개의 프로세스 동시에 작동

                                    
    if(len(sys.argv) == 0):
        print("plese set two argument :: Annual(A), Quarter(Q) / kospi -> 1 + kosdaq -> 2 + konex -> 4")
    elif(len(sys.argv) == 3):
        if(sys.argv[1] == 'A' or sys.argv[1] == 'Annual'):
            Insert_DB_Afinance(int(sys.argv[2]))
        if(sys.argv[1] == 'Q' or sys.argv[1] == 'Quarter'):
            #Insert_DB_Qfinance(int(sys.argv[2]))
            pool.starmap(multiprocess, [x for x in [[x,int(sys.argv[2])] for x in range(0,len(kospi),execute_size)]])
    else:
        print("plese set two argument :: Annual(A), Quarter(Q) / kospi -> 1 + kosdaq -> 2 + konex -> 4")
    print("실행 시간 : %s초" % (time.time() - start_time))