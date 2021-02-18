import sys

import pymysql
from DB_setting import *
import pandas as pd

import time
import datetime
import FinanceDataReader as fdr

import GetFinancialStatements as GF
import GetStockInfo as GS

KOSPI = 1
KOSDAQ = 2
KONEX = 4

execute_size = 100

def Get_invest_indicators(recent_data, totalnum, price, date):
    #print(recent_data)
    # print(price)
    # PER
    record = [None for i in range(4)]
    if (recent_data[0] != "\xa0"):
        if (recent_data[0] != "0" or totalnum == 0):
            PER = float(price / (float(recent_data[0].replace(',', '')) * 100000 / totalnum))
            record[0] = str(round(PER, 2))

    # PBR
    if (recent_data[2] != "\xa0" and recent_data[3] != "\xa0"):
        if (recent_data[2] != recent_data[3]):
            PBR = float(price / ((float(recent_data[2].replace(',', '')) - int(recent_data[3].replace(',', ''))) * 100000 / totalnum))
            record[1] = str(round(PBR, 2))

    # PSR
    if (recent_data[4] != "\xa0"):
        if (recent_data[4] != "0"):
            PSR = float(price / (float(recent_data[4].replace(',', '')) * 100000 / totalnum))
            record[2] = str(round(PSR, 2))

    # Year
    record[3] = date
    
    return record


"""
실적 예상값이 없을때 사용하는 함수
"""
def Get_ratio(finance):
    #print(finance)
    record = [None for i in range(8)]

    #흑흑 BB / 흑적 BR / 적흑 RB / 적적 RR
    #YOY
    if(finance[-5][7] != "\xa0"):  #보안필요
        if(finance[-5][7] == "0"):
            finance[-5][7] = "1"
        YOY = (float(finance[-1][7].replace(',', '')) - float(finance[-5][7].replace(',', ''))) / abs(float(float(finance[-5][7].replace(',', ''))))
        record[0] = str(round(YOY * 100, 2))
        if(int(finance[-5][7].replace(',', '')) <= 0):
            record[1] = "R"
        else:
            record[1] = "B"
        if(int(finance[-1][7].replace(',', '')) <= 0):
            record[1] += "R"
        else:
            record[1] += "B"
        
    #QoQ
    if(finance[-2][7] != "\xa0"):
        if(finance[-2][7] == "0"):
            finance[-2][7] = "1"
        QoQ = (float(finance[-1][7].replace(',', '')) - float(finance[-2][7].replace(',', ''))) / abs(float(float(finance[-2][7].replace(',', ''))))
        record[2] = str(round(QoQ * 100, 2))
        if(int(finance[-2][7].replace(',', '')) <= 0):
            record[3] = "R"
        else:
            record[3] = "B"
        if(int(finance[-1][7].replace(',', '')) <= 0):
            record[3] += "R"
        else:
            record[3] += "B"
    #EYoY
    #record[2] = None #NAN
    #EQoQ
    #record[3] = None
    return record


"""
실적 예상값이 있을때 사용하는 함수
"""
def Get_Eratio(finance, finance_E):
    #print(finance)
    #print(finance_E)
    record = [None for i in range(8)]
    
    #흑흑 BB / 흑적 BR / 적흑 RB / 적적 RR
    #YOY
    if(finance[-5][7] != "\xa0"):  #보안필요
        if(finance[-5][7] == "0"):
            finance[-5][7] = "1"
        YOY = (float(finance[-1][7].replace(',', '')) - float(finance[-5][7].replace(',', ''))) / abs(float(int(finance[-5][7].replace(',', ''))))
        record[0] = str(round(YOY * 100, 2))
        if(int(finance[-5][7].replace(',', '')) <= 0):
            record[1] = "R"
        else:
            record[1] = "B"
        if(int(finance[-1][7].replace(',', '')) <= 0):
            record[1] += "R"
        else:
            record[1] += "B"
        
    #QoQ
    if(finance[-2][7] != "\xa0"):
        if(finance[-2][7] == "0"):
            finance[-2][7] = "1"
        QoQ = (float(finance[-1][7].replace(',', '')) - float(finance[-2][7].replace(',', ''))) / abs(float(int(finance[-2][7].replace(',', ''))))
        record[2] = str(round(QoQ * 100, 2))
        
        if(int(finance[-2][7].replace(',', '')) <= 0):
            record[3] = "R"
        else:
            record[3] = "B"
        if(int(finance[-1][7].replace(',', '')) <= 0):
            record[3] += "R"
        else:
            record[3] += "B"
            

    #EYoY 현재기준 다음분기 예측 상승량
    if(finance_E[0][7] != "\xa0" and finance[-4][7] != "\xa0"):
        if(finance[-4][7] == "0"):
            finance[-4][7] = "1"
        EYoY = (float(finance_E[0][7].replace(',', '')) - float(finance[-4][7].replace(',', ''))) / abs(float(int(finance[-4][7].replace(',', ''))))
        record[4] = str(round(EYoY * 100, 2))
        
        if(int(finance[-4][7].replace(',', '')) <= 0):
            record[5] = "R"
        else:
            record[5] = "B"
        if(int(finance_E[0][7].replace(',', '')) <= 0):
            record[5] += "R"
        else:
            record[5] += "B"
    #EQoQ
    if(finance_E[0][7] != "\xa0" and finance[-1][7] != "\xa0"):
        if(finance[-1][7] == "0"):
            finance[-1][7] = "1"
        EQoQ = (float(finance_E[0][7].replace(',', '')) - float(finance[-1][7].replace(',', ''))) / abs(float(int(finance[-1][7].replace(',', ''))))
        record[6] = str(round(EQoQ * 100, 2))
        
        if(int(finance[-1][7].replace(',', '')) <= 0):
            record[7] = "R"
        else:
            record[7] = "B"
        if(int(finance_E[0][7].replace(',', '')) <= 0):
            record[7] += "R"
        else:
            record[7] += "B"
    return record


# Sector Kospi_info, Kosdaq_info, Konex_info
def Get_DB_info(Sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM " + Sector)
    stock = cursor.fetchall()
    return stock


def Insert_DB_invest(sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    totalnum = 0

    kospi_record = []
    kosdaq_record = []
    konex_record = []

    #시간설정
    #now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    now = time.strftime('%Y-%m', time.localtime(time.time()))

    if(sector % 2 == 1):
        kospi = Get_DB_info("Kospi_info")
        cursor.execute(
                "SELECT Code,Date,NetIncome,NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount,OperatingProfit FROM Kospi_Qfinance"
            )
        finance_data = cursor.fetchall()
        finance_df = pd.DataFrame(finance_data)
        #print(df)

        for num , i in enumerate(kospi):
            # if(num > 50):
            #     return
            #     continue
            # if(i["Code"] != "000390"):
            #      continue
            print("[{} / {}] {}".format(num + 1, len(kospi), i["Code"]))
            price_df = fdr.DataReader(i["Code"],now)
            try:
                price = price_df["Close"].tail(1)[0]
            except:
                print("NO price")
                continue
            record = [i["Name"], i["Code"]]
            record.extend(" ")
            record[2] = str(price)
            # print(record)

            code_df = finance_df[finance_df['Code'].str.contains(i["Code"])]
            rs_df = code_df[~code_df['Date'].str.contains("\(E\)") & ~code_df['Date'].str.contains("\(P\)")]
            rs_df2 = code_df[code_df['Date'].str.contains("\(E\)") | code_df['Date'].str.contains("\(P\)")]
            
            #print(rs_df.values,df_flag,df_Eflag)
            if (len(rs_df) != 0):    #데이터가 없음
                df_flag = rs_df.values[-1]
                df_Eflag = rs_df2.values[0]
                #주식 발행 수 문제
                if (rs_df.values[-1][3] == "0" or rs_df.values[-1][3] == "\xa0"):
                    print(rs_df.values)
                    print("Value error : have not data (pass)")
                    continue
                else:
                    totalnum = int(rs_df.values[-1][3].replace(',', ''))


                #예상치 결측 문제 없다면 실적발표 값으로 설정
                #Code Date NetIncome NumOutstandingShares 
                #TotalAsset TotalDebt SalesAccount OperatingProfit
                if (rs_df2.values[0][2] == "\xa0" or rs_df2.values[0][6] == "\xa0"):
                    # 결측임
                    record[len(record):] = Get_invest_indicators(rs_df.values[-1][2:], totalnum, price, rs_df.values[-1][1])
                    
                else:
                    # 총자산 총부채만 지난 데이터로 사용
                    # print("Value error : finance_value : trying last year")
                    temp = list(rs_df2.values[0][2:4])
                    temp += list(rs_df.values[-1][4:6])
                    temp += list(rs_df2.values[0][6:])
                    record[len(record):] = Get_invest_indicators(temp, totalnum, price, rs_df2.values[0][1])

                #print(rs_df2.values)
                #YoY QoQ EYoY EQoQ 계산 7:OperatingProfit
                if (rs_df2.values[0][2] == "\xa0" and rs_df2.values[0][7] == "\xa0"):
                    # 결측임
                    record[len(record):] = Get_ratio(rs_df.values)
                else:
                    record[len(record):] = Get_Eratio(rs_df.values, rs_df2.values)

                str_now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                record.append(str_now)
                print(record)
                kospi_record.append(record)
                
                if(num % execute_size == execute_size-1):
                    cursor.executemany("INSERT INTO Kospi_qinvest_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",kospi_record)
                    kospi_record = []
                    con.commit()
            else:
                print("No data!!")
        cursor.executemany("INSERT INTO Kospi_qinvest_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",kospi_record)
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        kosdaq = Get_DB_info("Kosdaq_info")
        cursor.execute(
                "SELECT Code,Date,NetIncome,NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount,OperatingProfit FROM Kosdaq_Qfinance"
            )
        finance_data = cursor.fetchall()
        finance_df = pd.DataFrame(finance_data)
        #print(df)
        
        for num,i in enumerate(kosdaq):
            print("[{} / {}] {}".format(num + 1, len(kosdaq), i["Code"]))
            price_df = fdr.DataReader(i["Code"],now)
            try:
                price = price_df["Close"].tail(1)[0]
            except:
                print("NO price")
                continue
            record = [i["Name"], i["Code"]]
            record.extend(" ")
            record[2] = str(price)
            # print(record)
            
            code_df = finance_df[finance_df['Code'].str.contains(i["Code"])]
            rs_df = code_df[~code_df['Date'].str.contains("\(E\)") & ~code_df['Date'].str.contains("\(P\)")]
            rs_df2 = code_df[code_df['Date'].str.contains("\(E\)") | code_df['Date'].str.contains("\(P\)")]
            
            # print(rs_df.values)
            # print(len(rs_df))
            # print(rs_df.values[0][3])

            if (len(rs_df) != 0):
                #주식 발행 수 문제
                if (rs_df.values[-1][3] == "0" or rs_df.values[-1][3] == "\xa0"):
                    print(rs_df.values)
                    print("Value error : have not data (pass)")
                    continue
                else:
                    totalnum = int(rs_df.values[-1][3].replace(',', ''))

                #예상치 결측 문제 없다면 실적발표 값으로 설정
                #Code Date NetIncome NumOutstandingShares 
                #TotalAsset TotalDebt SalesAccount OperatingProfit
                if (rs_df2.values[0][2] == "\xa0" or rs_df2.values[0][6] == "\xa0"):
                    # 결측임
                    record[len(record):] = Get_invest_indicators(rs_df.values[-1][2:], totalnum, price, rs_df.values[-1][1])
                    
                else:
                    # 총자산 총부채만 지난 데이터로 사용
                    # print("Value error : finance_value : trying last year")
                    temp = list(rs_df2.values[0][2:4])
                    temp += list(rs_df.values[-1][4:6])
                    temp += list(rs_df2.values[0][6:])
                    record[len(record):] = Get_invest_indicators(temp, totalnum, price, rs_df2.values[0][1])

                #print(rs_df2.values)
                #YoY QoQ EYoY EQoQ 계산 7:OperatingProfit
                if (rs_df2.values[0][2] == "\xa0" and rs_df2.values[0][7] == "\xa0"):
                    # 결측임
                    record[len(record):] = Get_ratio(rs_df.values)
                else:
                    record[len(record):] = Get_Eratio(rs_df.values, rs_df2.values)

                str_now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                record.append(str_now)
                print(record)
                kospi_record.append(record)
                if(num % execute_size == execute_size-1):
                    cursor.executemany("INSERT INTO Kosdaq_qinvest_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",kospi_record)
                    kospi_record = []
                    con.commit()
            else:
                print("No data!!")
        cursor.executemany("INSERT INTO Kosdaq_qinvest_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",kospi_record)
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        konex = Get_DB_info("Konex_info")
        cursor.execute(
                "SELECT Code,Date,NetIncome,NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount,OperatingProfit FROM Konex_Qfinance"
            )
        finance_data = cursor.fetchall()
        finance_df = pd.DataFrame(finance_data)
        #print(df)
        
        for num,i in enumerate(konex):
            print("[{} / {}] {}".format(num + 1, len(konex), i["Code"]))
            price_df = fdr.DataReader(i["Code"],now)
            try:
                price = price_df["Close"].tail(1)[0]
            except:
                print("NO price")
                continue
            record = [i["Name"], i["Code"]]
            record.extend(" ")
            record[2] = str(price)
            # print(record)
            
            code_df = finance_df[finance_df['Code'].str.contains(i["Code"])]
            rs_df = code_df[~code_df['Date'].str.contains("\(E\)") & ~code_df['Date'].str.contains("\(P\)")]
            rs_df2 = code_df[code_df['Date'].str.contains("\(E\)") | code_df['Date'].str.contains("\(P\)")]
            
            # print(rs_df.values)
            # print(len(rs_df))
            # print(rs_df.values[0][3])

            if (len(rs_df) != 0):
                #주식 발행 수 문제
                if (rs_df.values[-1][3] == "0" or rs_df.values[-1][3] == "\xa0"):
                    print(rs_df.values)
                    print("Value error : have not data (pass)")
                    continue
                else:
                    totalnum = int(rs_df.values[-1][3].replace(',', ''))

                #예상치 결측 문제 없다면 실적발표 값으로 설정
                #Code Date NetIncome NumOutstandingShares 
                #TotalAsset TotalDebt SalesAccount OperatingProfit
                if (rs_df2.values[0][2] == "\xa0" or rs_df2.values[0][6] == "\xa0"):
                    # 결측임
                    record[len(record):] = Get_invest_indicators(rs_df.values[-1][2:], totalnum, price, rs_df.values[-1][1])
                    
                else:
                    # 총자산 총부채만 지난 데이터로 사용
                    # print("Value error : finance_value : trying last year")
                    temp = list(rs_df2.values[0][2:4])
                    temp += list(rs_df.values[-1][4:6])
                    temp += list(rs_df2.values[0][6:])
                    record[len(record):] = Get_invest_indicators(temp, totalnum, price, rs_df2.values[0][1])

                #print(rs_df2.values)
                #YoY QoQ EYoY EQoQ 계산 7:OperatingProfit
                if (rs_df2.values[0][2] == "\xa0" and rs_df2.values[0][7] == "\xa0"):
                    # 결측임
                    record[len(record):] = Get_ratio(rs_df.values)
                else:
                    record[len(record):] = Get_Eratio(rs_df.values, rs_df2.values)

                str_now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                record.append(str_now)
                print(record)
                kospi_record.append(record)
                if(num % execute_size == execute_size-1):
                    cursor.executemany("INSERT INTO Konex_qinvest_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",kospi_record)
                    kospi_record = []
                    con.commit()
            else:
                print("No data!!")
        cursor.executemany("INSERT INTO Konex_qinvest_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",kospi_record)
        con.commit()
    con.close()


if __name__ == "__main__":
    if(len(sys.argv) == 0):
        print("plese set three argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4")
    elif(len(sys.argv) == 2):
        Insert_DB_invest(int(sys.argv[1]))
    else:
        print("plese set three argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4")
