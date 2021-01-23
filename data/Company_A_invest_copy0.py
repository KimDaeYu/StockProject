import sys

import pymysql
from DB_setting import *
import pandas as pd

import time
import FinanceDataReader as fdr

import GetFinancialStatements as GF
import GetStockInfo as GS

KOSPI = 1
KOSDAQ = 2
KONEX = 4

execute_size = 100

def Get_invest_indicators(recent_data, totalnum, price, year):
    # print(recent_data)
    # print(price)
    # PER
    record = ["NAN" for i in range(4)]
    if (recent_data[0] != "\xa0"):
        if (recent_data[0] != "0" or totalnum == 0):
            PER = float(price / float(int(recent_data[0].replace(',', '')) * 100000 / totalnum))
            record[0] = str(round(PER, 2))

    # PBR
    if (recent_data[2] != "\xa0" and recent_data[3] != "\xa0"):
        if (recent_data[2] != recent_data[3]):
            PBR = float(price / float((int(recent_data[2].replace(',', '')) - int(
                recent_data[3].replace(',', ''))) * 100000 / totalnum))
            record[1] = str(round(PBR, 2))

    # PSR
    if (recent_data[4] != "\xa0"):
        if (recent_data[4] != "0"):
            PSR = float(price / float(int(recent_data[4].replace(',', '')) * 100000 / totalnum))
            record[2] = str(round(PSR, 2))

    # Year
    record[3] = year
    
    return record


# Sector Kospi_info, Kosdaq_info, Konex_info
def Get_DB_info(Sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM " + Sector)
    stock = cursor.fetchall()
    return stock


def Insert_DB_invest(parayear, sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    totalnum = 0
    
    year = str(parayear)

    kospi_record = []
    kosdaq_record = []
    konex_record = []

    #시간설정
    #now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    now = time.strftime('%Y-%m', time.localtime(time.time()))
    
    if(sector % 2 == 1):
        kospi = Get_DB_info("Kospi_info")
        cursor.execute(
                "SELECT Code,Date,NetIncome,NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Kospi_Afinance"
            )
        finance_data = cursor.fetchall()
        finance_df = pd.DataFrame(finance_data)
        #print(df)
        
        for num , i in enumerate(kospi):
            if(num < 792):
                continue
            year = str(parayear)
            print("[{} / {}] {}".format(num + 1, len(kospi), i["Code"]))
            price_df = fdr.DataReader(i["Code"],now)
            price = price_df["Close"].tail(1)[0]
            
            record = [i["Name"], i["Code"]]
            record.extend(" ")
            record[2] = str(price)
            # print(record)
            
            code_df = finance_df[finance_df['Code'].str.contains(i["Code"])]
            rs_df = code_df[code_df['Date'].str.contains(year)]
            
            year = str(int(year) - 1) #추후에 year값도 저장
            rs_df2 = code_df[code_df['Date'].str.contains(year)]
            
            print(rs_df.values)
            # print(len(rs_df))
            # print(rs_df.values[0][3])

            if (len(rs_df) != 0):
                #주식 발행 수 문제
                if (rs_df.values[0][3] == "0" or rs_df.values[0][3] == "\xa0"):
                    # print("Value error : totalnum : trying last year")
                    
                    # print(rs_df2.values)
                    if (rs_df2.values[0][2] == "0" or rs_df2.values[0][2] == "\xa0"):
                        print("Value error : have not data (pass)")
                        continue
                    totalnum = int(rs_df2.values[0][3].replace(',', ''))
                else:
                    totalnum = int(rs_df.values[0][3].replace(',', ''))

                    
                #예상치 결측 문제
                if (rs_df.values[0][2] == "\xa0" or (rs_df.values[0][4] == "\xa0" and rs_df.values[0][5])):
                    # print("Value error : finance_value : trying last year")
                    record[len(record):] = Get_invest_indicators(rs_df2.values[0][2:], totalnum, price, year)
                    print(record)
                else:
                    # print("Value error : finance_value : trying last year")
                    year = str(int(year) + 1)
                    record[len(record):] = Get_invest_indicators(rs_df.values[0][2:], totalnum, price, year)
                    print(record)
                kospi_record.append(record)
                
                if(num % execute_size == execute_size-1):
                    cursor.executemany("INSERT INTO Kospi_invest_info VALUES(%s,%s,%s,%s,%s,%s,%s)",kospi_record)
                    kospi_record = []
                    con.commit()
            else:
                print("No data!!")
        cursor.executemany("INSERT INTO Kospi_invest_info VALUES(%s,%s,%s,%s,%s,%s,%s)",kospi_record)
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        kosdaq = Get_DB_info("Kosdaq_info")
        cursor.execute(
                "SELECT Code,Date,NetIncome,NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Kosdaq_Afinance"
            )
        finance_data = cursor.fetchall()
        finance_df = pd.DataFrame(finance_data)
        #print(df)
        
        for num,i in enumerate(kosdaq):
            year = str(parayear)
            print("[{} / {}] {}".format(num + 1, len(kosdaq), i["Code"]))
            price_df = fdr.DataReader(i["Code"],now)
            price = price_df["Close"].tail(1)[0]
            
            record = [i["Name"], i["Code"]]
            record.extend(" ")
            record[2] = str(price)
            # print(record)
            
            code_df = finance_df[finance_df['Code'].str.contains(i["Code"])]
            rs_df = code_df[code_df['Date'].str.contains(year)]
            
            year = str(int(year) - 1) #추후에 year값도 저장
            rs_df2 = code_df[code_df['Date'].str.contains(year)]
            
            # print(rs_df.values)
            # print(len(rs_df))
            # print(rs_df.values[0][3])

            if (len(rs_df) != 0):
                #주식 발행 수 문제
                if (rs_df.values[0][3] == "0" or rs_df.values[0][3] == "\xa0"):
                    # print("Value error : totalnum : trying last year")
                    
                    # print(rs_df2.values)
                    if (rs_df2.values[0][2] == "0" or rs_df2.values[0][2] == "\xa0"):
                        # print("Value error : have not data (pass)")
                        continue
                    totalnum = int(rs_df2.values[0][3].replace(',', ''))
                else:
                    totalnum = int(rs_df.values[0][3].replace(',', ''))

                    
                #예상치 결측 문제
                if (rs_df.values[0][2] == "\xa0" or (rs_df.values[0][4] == "\xa0" and rs_df.values[0][5])):
                    # print("Value error : finance_value : trying last year")
                    record[len(record):] = Get_invest_indicators(rs_df2.values[0][2:], totalnum, price, year)
                    print(record)
                else:
                    # print("Value error : finance_value : trying last year")
                    year = str(int(year) + 1)
                    record[len(record):] = Get_invest_indicators(rs_df.values[0][2:], totalnum, price, year)
                    print(record)
                kospi_record.append(record)
                
                if(num % execute_size == execute_size-1):
                    cursor.executemany("INSERT INTO Kosdaq_invest_info VALUES(%s,%s,%s,%s,%s,%s,%s)",kospi_record)
                    kospi_record = []
                    con.commit()
            else:
                print("No data!!")
        cursor.executemany("INSERT INTO Kosdaq_invest_info VALUES(%s,%s,%s,%s,%s,%s,%s)",kosdaq_record)
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        konex = Get_DB_info("Konex_info")
        cursor.execute(
                "SELECT Code,Date,NetIncome,NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Konex_Afinance"
            )
        finance_data = cursor.fetchall()
        finance_df = pd.DataFrame(finance_data)
        #print(df)
        
        for num,i in enumerate(konex):
            year = str(parayear)
            print("[{} / {}] {}".format(num + 1, len(konex), i["Code"]))
            price_df = fdr.DataReader(i["Code"],now)
            price = price_df["Close"].tail(1)[0]
            
            record = [i["Name"], i["Code"]]
            record.extend(" ")
            record[2] = price
            # print(record)
            
            code_df = finance_df[finance_df['Code'].str.contains(i["Code"])]
            rs_df = code_df[code_df['Date'].str.contains(year)]
            
            year = str(int(year) - 1) #추후에 year값도 저장
            rs_df2 = code_df[code_df['Date'].str.contains(year)]
            
            # print(rs_df.values)
            # print(len(rs_df))
            # print(rs_df.values[0][3])

            if (len(rs_df) != 0):
                #주식 발행 수 문제
                if (rs_df.values[0][3] == "0" or rs_df.values[0][3] == "\xa0"):
                    # print("Value error : totalnum : trying last year")
                    
                    # print(rs_df2.values)
                    if (rs_df2.values[0][2] == "0" or rs_df2.values[0][2] == "\xa0"):
                        # print("Value error : have not data (pass)")
                        continue
                    totalnum = int(rs_df2.values[0][3].replace(',', ''))
                else:
                    totalnum = int(rs_df.values[0][3].replace(',', ''))

                    
                #예상치 결측 문제
                if (rs_df.values[0][2] == "\xa0" or (rs_df.values[0][4] == "\xa0" and rs_df.values[0][5])):
                    # print("Value error : finance_value : trying last year")
                    record[len(record):] = Get_invest_indicators(rs_df2.values[0][2:], totalnum, price, year)
                    print(record)
                else:
                    # print("Value error : finance_value : trying last year")
                    year = str(int(year) + 1)
                    record[len(record):] = Get_invest_indicators(rs_df.values[0][2:], totalnum, price, year)
                    print(record)
                kospi_record.append(record)
                
                if(num % execute_size == execute_size-1):
                    cursor.executemany("INSERT INTO Kosdaq_invest_info VALUES(%s,%s,%s,%s,%s,%s,%s)",kospi_record)
                    kospi_record = []
                    con.commit()
            else:
                print("No data!!")
        cursor.executemany("INSERT INTO Konex_invest_info VALUES(%s,%s,%s,%s,%s,%s,%s)",konex_record)     
        con.commit()
    con.close()


    
    
    
def Insert_DB_exp_invest(parayear,sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    totalnum = 0

    year = str(parayear)

    kospi_record = []
    kosdaq_record = []
    konex_record = []

    if(sector % 2 == 1):
        kospi = Get_DB_info("Kospi_info")
        data = []
        for num , i in enumerate(kospi):
            year = str(parayear)
            print("[{} / {}] {}".format(num + 1, len(kospi), i["Code"]))
            temp = GF.StockFinance(i['Code'])
            temp.getPrice()

            record = [i['Name'], i['Code']]
            record.extend(" ")
            record[2] = temp.Price["Price"]

            price = int(record[2].replace(',', ''))
            cursor.execute(
                "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Kospi_Afinance WHERE Code = %s AND Date like %s",
                (i['Code'], year + "%")
            )
            recent_data = cursor.fetchall()
            cursor.execute(
                "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Kospi_Afinance WHERE Code = %s AND Date like %s",
                (i['Code'], str(parayear-1) + "%")
            )
            recent_data2 = cursor.fetchall()
            if (len(recent_data) != 0):
                recent_data[0] = list(recent_data[0].values())
                if(recent_data[0][1] == "\xa0"):
                    recent_data2[0] = list(recent_data2[0].values())
                    if (recent_data2[0][1] == "0" or recent_data2[0][1] == "\xa0"):
                        print("Value error : have not data (pass)")
                        continue
                    totalnum = int(recent_data2[0][1].replace(',', ''))
                else:
                    totalnum = int(recent_data[0][1].replace(',', ''))

                record[len(record):] = Get_invest_indicators(recent_data, totalnum, price, year)
                print(record)
                kospi_record.append(record)
                del(temp)
                if(num % execute_size == execute_size-1):
                    cursor.executemany("INSERT INTO Kospi_exp_invest_info VALUES(%s,%s,%s,%s,%s,%s,%s)",kospi_record)
                    kospi_record = []
                    con.commit()
            else:
                print("No data!!")
        cursor.executemany("INSERT INTO Kospi_exp_invest_info VALUES(%s,%s,%s,%s,%s,%s,%s)",kospi_record)
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        kosdaq = Get_DB_info("Kosdaq_info")
        for num,i in enumerate(kosdaq):
            year = str(parayear)
            print("[{} / {}] {}".format(num,len(kosdaq), i['Code']))
            temp = GF.StockFinance(i['Code'])
            temp.getPrice()

            record = [i['Name'], i['Code']]
            record.extend(" ")
            record[2] = temp.Price["Price"]

            price = int(record[2].replace(',', ''))
            cursor.execute(
                "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Kosdaq_Afinance WHERE Code = %s AND Date like %s",
                (i['Code'], year + "%")
            )
            recent_data = cursor.fetchall()
            
            cursor.execute(
                "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Kosdaq_Afinance WHERE Code = %s AND Date like %s",
                (i['Code'], str(parayear-1) + "%")
            )
            recent_data2 = cursor.fetchall()
            
            if (len(recent_data) != 0):
                recent_data[0] = list(recent_data[0].values())
                if(recent_data[0][1] == "\xa0"):
                    recent_data2[0] = list(recent_data2[0].values())
                    if (recent_data2[0][1] == "0" or recent_data2[0][1] == "\xa0"):
                        print("Value error : have not data (pass)")
                        continue
                    totalnum = int(recent_data2[0][1].replace(',', ''))
                else:
                    totalnum = int(recent_data[0][1].replace(',', ''))

                record[len(record):] = Get_invest_indicators(recent_data, totalnum, price, year)
                print(record)
                kosdaq_record.append(record)
                del(temp)
                if(num % execute_size == execute_size-1):
                    cursor.executemany("INSERT INTO Kosdaq_exp_invest_info VALUES(%s,%s,%s,%s,%s,%s,%s)",kosdaq_record)
                    kosdaq_record = []
                    con.commit()
            else:
                print("No data!!")
        cursor.executemany("INSERT INTO Kosdaq_exp_invest_info VALUES(%s,%s,%s,%s,%s,%s,%s)",kosdaq_record)
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        konex = Get_DB_info("Konex_info")
        for num,i in enumerate(konex):
            year = str(parayear)
            print("[{} / {}] {}".format(num,len(konex),i['Code']))
            temp = GF.StockFinance(i["Code"])
            temp.getPrice()

            record = [i["Name"], i["Code"]]
            record.extend(" ")
            record[2] = temp.Price["Price"]

            price = int(record[2].replace(',', ''))
            cursor.execute(
                "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Konex_Afinance WHERE Code = %s AND Date like %s",
                (i['Code'], year + "%")
            )
            recent_data = cursor.fetchall()

            cursor.execute(
                "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Konex_Afinance WHERE Code = %s AND Date like %s",
                (i['Code'], str(parayear-1) + "%")
            )
            recent_data2 = cursor.fetchall()

            if (len(recent_data) != 0):
                recent_data[0] = list(recent_data[0].values())
                if(recent_data[0][1] == "\xa0"):
                    recent_data2[0] = list(recent_data2[0].values())
                    if (recent_data2[0][1] == "0" or recent_data2[0][1] == "\xa0"):
                        print("Value error : have not data (pass)")
                        continue
                    totalnum = int(recent_data2[0][1].replace(',', ''))
                else:
                    totalnum = int(recent_data[0][1].replace(',', ''))
                                           
                record[len(record):] = Get_invest_indicators(recent_data, totalnum, price, year)
                print(record)
                konex_record.append(record)
                del(temp)
                if(num % execute_size == execute_size-1):
                    cursor.executemany("INSERT INTO Konex_exp_invest_info VALUES(%s,%s,%s,%s,%s,%s,%s)",konex_record)
                    konex_record = []
                    con.commit()
            else:
                print("No data!!")
        cursor.executemany("INSERT INTO Konex_exp_invest_info VALUES(%s,%s,%s,%s,%s,%s,%s)",konex_record)     
        con.commit()
    con.close()


if __name__ == "__main__":
    if(len(sys.argv) == 0):
        print("plese set three argument :: Present(P), Expect(E) / year / kospi -> 1 + kosdaq -> 2 + konex -> 4")
    elif(len(sys.argv) == 4):
        if(sys.argv[1] == 'P' or sys.argv[1] == 'Present'):
            Insert_DB_invest(int(sys.argv[2]),int(sys.argv[3]))
        if(sys.argv[1] == 'E' or sys.argv[1] == 'Expect'):
            Insert_DB_exp_invest(int(sys.argv[2]),int(sys.argv[3]))
    else:
        print("plese set three argument :: Present(P), Expect(E) / year / kospi -> 1 + kosdaq -> 2 + konex -> 4")
