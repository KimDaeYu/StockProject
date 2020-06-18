import GetFinancialStatements as GF
import GetStockInfo as GS

import pymysql

KOSPI = 1
KOSDAQ = 2
KONEX = 4



def Connect_DB():
    con = pymysql.connect(
        user='stock', 
        passwd='12345678',
        host='127.0.0.1', 
        db='stock_db', 
        charset='utf8'
    )
    return con

def Reset_DB(sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)

    if (sector % 2 is 1):
        cursor.execute("""
        DROP TABLE IF EXISTS Kospi_info;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Kospi_Qfinance;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Kospi_Afinance;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Kospi_invest_info;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Kospi_exp_invest_info;
          """)
        con.commit()
        
    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        cursor.execute("""
        DROP TABLE IF EXISTS Kosdaq_info;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Kosdaq_Qfinance;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Kosdaq_Afinance;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Kosdaq_invest_info;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Kosdaq_exp_invest_info;
          """)
        con.commit()
    
    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        cursor.execute("""
        DROP TABLE IF EXISTS Konex_info;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Konex_Qfinance;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Konex_Afinance;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Konex_invest_info;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Konex_exp_invest_info;
          """)
        con.commit()
    con.close()
    
def Create_DB(sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    
    if (sector % 2 is 1):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kospi_info` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Business`	TEXT,
        `Product`	TEXT,
        `Listed_Date`	TEXT,
        `Settlement_Date`	TEXT,
        `Representative_Name`	TEXT,
        `Homepage`	TEXT,
        `Region`	TEXT,
         PRIMARY KEY (`Code`)
            ); 
            """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kospi_Qfinance` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Date`	TEXT,
        `SalesAccount`	TEXT,
        `OperatingProfit`	TEXT,
        `OperatingProfit_Official`	TEXT,
        `NetIncome`	TEXT,
        `CSNI`	TEXT,
        `NCSNI`	TEXT,
        `TotalAsset`	TEXT,
        `TotalDebt`	TEXT,
        `TotalCapital`	TEXT,
        `ConShare`	TEXT,
        `NConShare`	TEXT,
        `CashCapital`	TEXT,
        `DebtRatio`	TEXT,
        `ReserveRatio`	TEXT,
        `BusinessProfitRatio`	TEXT,
        `CSNetProfitRatio`	TEXT,
        `ROA`	TEXT,
        `ROE`	TEXT,
        `EPS`	TEXT,
        `BPS`	TEXT,
        `DPS`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `NumOutstandingShares`	TEXT,
        `DividendYieldRatio`	TEXT,
        PRIMARY KEY (`Code`)
         );""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kospi_Afinance` (
        `Name`	VARCHAR(25) NOT NULL,
         `Code`	VARCHAR(10) NOT NULL,
        `Date`	TEXT,
        `SalesAccount`	TEXT,
        `OperatingProfit`	TEXT,
        `OperatingProfit_Official`	TEXT,
        `NetIncome`	TEXT,
        `CSNI`	TEXT,
        `NCSNI`	TEXT,
        `TotalAsset`	TEXT,
        `TotalDebt`	TEXT,
        `TotalCapital`	TEXT,
        `ConShare`	TEXT,
        `NConShare`	TEXT,
        `CashCapital`	TEXT,
        `DebtRatio`	TEXT,
        `ReserveRatio`	TEXT,
        `BusinessProfitRatio`	TEXT,
        `CSNetProfitRatio`	TEXT,
        `ROA`	TEXT,
        `ROE`	TEXT,
        `EPS`	TEXT,
        `BPS`	TEXT,
        `DPS`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `NumOutstandingShares`	TEXT,
        `DividendYieldRatio`	TEXT,
          PRIMARY KEY (`Code`)
            );""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kospi_invest_info` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Price`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `PSR`	TEXT,
         PRIMARY KEY (`Code`)
           );  """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kospi_exp_invest_info` (
        `Name`	VARCHAR(25) NOT NULL,
         `Code`	VARCHAR(10) NOT NULL,
        `Price`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `PSR`	TEXT,
          PRIMARY KEY (`Code`)
            );  """)
        con.commit()
    
    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kosdaq_info` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Business`	TEXT,
        `Product`	TEXT,
        `Listed_Date`	TEXT,
        `Settlement_Date`	TEXT,
        `Representative_Name`	TEXT,
        `Homepage`	TEXT,
        `Region`	TEXT,
         PRIMARY KEY (`Code`)
          ); """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kosdaq_Qfinance` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Date`	TEXT,
        `SalesAccount`	TEXT,
        `OperatingProfit`	TEXT,
        `OperatingProfit_Official`	TEXT,
        `NetIncome`	TEXT,
        `CSNI`	TEXT,
        `NCSNI`	TEXT,
        `TotalAsset`	TEXT,
        `TotalDebt`	TEXT,
        `TotalCapital`	TEXT,
        `ConShare`	TEXT,
        `NConShare`	TEXT,
        `CashCapital`	TEXT,
        `DebtRatio`	TEXT,
        `ReserveRatio`	TEXT,
        `BusinessProfitRatio`	TEXT,
        `CSNetProfitRatio`	TEXT,
        `ROA`	TEXT,
        `ROE`	TEXT,
        `EPS`	TEXT,
        `BPS`	TEXT,
        `DPS`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `NumOutstandingShares`	TEXT,
        `DividendYieldRatio`	TEXT,
         PRIMARY KEY (`Code`)
         );""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kosdaq_Afinance` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Date`	TEXT,
        `SalesAccount`	TEXT,
        `OperatingProfit`	TEXT,
        `OperatingProfit_Official`	TEXT,
        `NetIncome`	TEXT,
        `CSNI`	TEXT,
        `NCSNI`	TEXT,
        `TotalAsset`	TEXT,
        `TotalDebt`	TEXT,
        `TotalCapital`	TEXT,
        `ConShare`	TEXT,
        `NConShare`	TEXT,
        `CashCapital`	TEXT,
        `DebtRatio`	TEXT,
        `ReserveRatio`	TEXT,
        `BusinessProfitRatio`	TEXT,
        `CSNetProfitRatio`	TEXT,
        `ROA`	TEXT,
        `ROE`	TEXT,
        `EPS`	TEXT,
        `BPS`	TEXT,
        `DPS`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `NumOutstandingShares`	TEXT,
        `DividendYieldRatio`	TEXT,
         PRIMARY KEY (`Code`)
         );""")       
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kosdaq_invest_info` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Price`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `PSR`	TEXT,
         PRIMARY KEY (`Code`)
         ); """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kosdaq_exp_invest_info` (
        `Name`	VARCHAR(25) NOT NULL,
         `Code`	VARCHAR(10) NOT NULL,
        `Price`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `PSR`	TEXT,
          PRIMARY KEY (`Code`)
          ); """)
        con.commit()
    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Konex_info` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Business`	TEXT,
        `Product`	TEXT,
        `Listed_Date`	TEXT,
        `Settlement_Date`	TEXT,
        `Representative_Name`	TEXT,
        `Homepage`	TEXT,
        `Region`	TEXT,
          PRIMARY KEY (`Code`)
            );  """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Konex_Qfinance` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Date`	TEXT,
        `SalesAccount`	TEXT,
        `OperatingProfit`	TEXT,
        `OperatingProfit_Official`	TEXT,
        `NetIncome`	TEXT,
        `CSNI`	TEXT,
        `NCSNI`	TEXT,
        `TotalAsset`	TEXT,
        `TotalDebt`	TEXT,
        `TotalCapital`	TEXT,
        `ConShare`	TEXT,
        `NConShare`	TEXT,
        `CashCapital`	TEXT,
        `DebtRatio`	TEXT,
        `ReserveRatio`	TEXT,
        `BusinessProfitRatio`	TEXT,
        `CSNetProfitRatio`	TEXT,
        `ROA`	TEXT,
        `ROE`	TEXT,
        `EPS`	TEXT,
        `BPS`	TEXT,
        `DPS`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `NumOutstandingShares`	TEXT,
        `DividendYieldRatio`	TEXT,
         PRIMARY KEY (`Code`)
         );""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Konex_Afinance` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Date`	TEXT,
        `SalesAccount`	TEXT,
        `OperatingProfit`	TEXT,
        `OperatingProfit_Official`	TEXT,
        `NetIncome`	TEXT,
        `CSNI`	TEXT,
        `NCSNI`	TEXT,
        `TotalAsset`	TEXT,
        `TotalDebt`	TEXT,
        `TotalCapital`	TEXT,
        `ConShare`	TEXT,
        `NConShare`	TEXT,
        `CashCapital`	TEXT,
        `DebtRatio`	TEXT,
        `ReserveRatio`	TEXT,
        `BusinessProfitRatio`	TEXT,
        `CSNetProfitRatio`	TEXT,
        `ROA`	TEXT,
        `ROE`	TEXT,
        `EPS`	TEXT,
        `BPS`	TEXT,
        `DPS`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `NumOutstandingShares`	TEXT,
        `DividendYieldRatio`	TEXT,
          PRIMARY KEY (`Code`)
          );""")     
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Konex_invest_info` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Price`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `PSR`	TEXT,
         PRIMARY KEY (`Code`)
         ); """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Konex_exp_invest_info` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Price`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `PSR`	TEXT,
         PRIMARY KEY (`Code`)
         ); """)
        con.commit()
    con.close()


    
    
def Insert_DB_info(sector):
    kosdaq_stocks = GS.download_stock_codes('kosdaq')
    kospi_stocks = GS.download_stock_codes('kospi')
    konex_stocks = GS.download_stock_codes('konex')

    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    
    if (sector % 2 is 1):
        for i in range(len(kospi_stocks)):
            #print(list(kosdaq_stocks.loc[i].fillna('')))
            cursor.execute("INSERT INTO Kospi_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", tuple(kospi_stocks.loc[i].fillna('')))
            con.commit()
            
    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        for i in range(len(kosdaq_stocks)):
            cursor.execute("INSERT INTO Kosdaq_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", tuple(kosdaq_stocks.loc[i].fillna('')))
            con.commit()
            
    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        for i in range(len(konex_stocks)):
            cursor.execute("INSERT INTO Konex_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", tuple(konex_stocks.loc[i].fillna('')))
            con.commit()
    con.close()

    
#Sector Kospi_info, Kosdaq_info, Konex_info
def Get_DB_info(Sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    #cursor.execute("SELECT * FROM Konex_info WHERE Name = ?;","유비온")
    cursor.execute("SELECT * FROM " + Sector)
    stock = cursor.fetchall()
    return stock


def Insert_DB_Qfinance(sector):
    kospi = Get_DB_info("Kospi_info")
    kosdaq = Get_DB_info("Kosdaq_info")
    konex = Get_DB_info("Konex_info")
    #print(kospi)
    
    
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)

    if(sector % 2 is 1):
        for i in kospi:
            temp = GF.StockFinance(i['Code'])
            temp.D_NetQuarterFinance()
            for j in temp.D_A:
                record = [i['Name'],i['Code'],j]
                record.extend(temp.D_A[j].values())
                if len(record) == 28:
                    cursor.execute("INSERT INTO Kospi_Qfinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", record)
            del(temp)
        con.commit()
        
    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        for i in kosdaq:
            temp = GF.StockFinance(i[1])
            temp.D_NetQuarterFinance()
            for j in temp.D_A:
                record = [i['Name'],i['Code'], j]
                record.extend(temp.D_A[j].values())
                if len(record) == 28:
                    cursor.execute("INSERT INTO Kosdaq_Qfinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",record)
            del (temp)
        con.commit()
    
    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        for i in konex:
            temp = GF.StockFinance(i[1])
            temp.D_NetQuarterFinance()
            for j in temp.D_A:
                record = [i['Name'],i['Code'], j]
                record.extend(temp.D_A[j].values())
                if len(record) == 28:
                    cursor.execute("INSERT INTO Konex_Qfinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",record)
            del (temp)
        con.commit()
    
    con.close()

def Insert_DB_Afinance(sector):
    kospi = Get_DB_info("Kospi_info")
    kosdaq = Get_DB_info("Kosdaq_info")
    konex = Get_DB_info("Konex_info")
    #print(kospi)
    
    
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    if(sector % 2 is 1):
        for i in kospi:
            temp = GF.StockFinance(i['Code'])
            temp.D_AnnualFinance()
            for j in temp.D_Y:
                record = [i['Name'],i['Code'],j]
                record.extend(temp.D_Y[j].values())
                if len(record) == 28:
                    cursor.execute("INSERT INTO Kospi_Afinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", record)
                    print(record)
            del(temp)
        con.commit()
    
    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        for i in kosdaq:
            temp = GF.StockFinance(i['Code'])
            temp.D_AnnualFinance()
            for j in temp.D_Y:
                record = [i['Name'],i['Code'],j]
                record.extend(temp.D_Y[j].values())
                if len(record) == 28:
                    cursor.execute("INSERT INTO Kosdaq_Afinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",record)
                    print(record)
            del (temp)
        con.commit()
    
    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        for i in konex:
            temp = GF.StockFinance(i['Code'])
            temp.D_AnnualFinance()
            for j in temp.D_Y:
                record = [i['Name'], i['Code'], j]
                record.extend(temp.D_Y[j].values())
                if len(record) == 28:
                    cursor.execute("INSERT INTO Konex_Afinance VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",record)
                    print(record)
            del (temp)
        con.commit()
        
    con.close()

def Insert_DB_invest(parayear,sector):
    kospi = Get_DB_info("Kospi_info")
    kosdaq = Get_DB_info("Kosdaq_info")
    konex = Get_DB_info("Konex_info")

    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    totalnum = 0

    year = str(parayear)

    kospi_record = []
    kosdaq_record = []
    konex_record = []

    
    if(sector % 2 is 1):
        for num , i in enumerate(kospi):
            print("[{} / {}] {}".format(num,len(kospi),i["Code"]))
            temp = GF.StockFinance(i["Code"])
            temp.getPrice()

            record = [i["Name"], i["Code"]]
            record.extend(" ")
            record[2] = temp.Price["Price"]

            price = int(record[2].replace(',', ''))
            cursor.execute(
                "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Kospi_Afinance WHERE Code = %s AND Date like %s",
                (i["Code"], year + "%")
            )
            recent_data = cursor.fetchall()
            if (len(recent_data) is not 0):
                recent_data[0] = list(recent_data[0].values())
                
                # if(len(kospi_record) is 5):            #테스트용
                #     break
                
                if (recent_data[0][0] is "0" or recent_data[0][1] is "\xa0"):
                    year =  str(int(year) - 1) #추후에 year값도 저장
                    cursor.execute(
                        "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Kospi_Afinance WHERE Code = %s AND Date like %s",
                        (i["Code"], year + "%")
                        )
                    recent_data2 = cursor.fetchall()
                    if (recent_data2[0][1] is "0" or recent_data2[0][1] is "\xa0"):
                        continue
                    recent_data2[0] = list(recent_data2[0].values())
                    recent_data[0] = recent_data2[0]
                    totalnum = int(recent_data2[0][1].replace(',', ''))
                else:
                    totalnum = int(recent_data[0][1].replace(',', ''))

                # PER
                record.extend(" ")
                if (recent_data[0][0] is not "\xa0"):
                    if (recent_data[0][0] is "0" or totalnum is 0):
                        continue
                    PER = float(price / float(int(recent_data[0][0].replace(',', '')) * 100000 / totalnum))
                    record[3] = str(round(PER, 2))

                # PBR
                record.extend(" ")
                if (recent_data[0][2] is not "\xa0" and recent_data[0][3] is not "\xa0"):
                    if (recent_data[0][2] is recent_data[0][3]):
                        continue
                    PBR = float(price / float((int(recent_data[0][2].replace(',', '')) - int(
                        recent_data[0][3].replace(',', ''))) * 100000 / totalnum))
                    record[4] = str(round(PBR, 2))

                # PSR
                record.extend(" ")
                if (recent_data[0][4] is not "\xa0"):
                    if (recent_data[0][4] is "0"):
                        continue
                    PSR = float(price / float(int(recent_data[0][4].replace(',', '')) * 100000 / totalnum))
                    record[5] = str(round(PSR, 2))

                print(record)
                kospi_record.extend(" ")
                kospi_record[len(kospi_record)-1] = record
                
                del (temp)
                
        for i in kospi_record:
            if len(i) == 6:
                cursor.execute("INSERT INTO Kospi_invest_info VALUES(%s,%s,%s,%s,%s,%s)", tuple(i))
            else:
                print("kospi :: worng format : " + i[0] + ", " + i[1])
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        
        for num,i in enumerate(kosdaq):
            print("[{} / {}] {}".format(num,len(kosdaq),i['Code']))
            temp = GF.StockFinance(i["Code"])
            temp.getPrice()
            
            record = [i["Name"], i["Code"]]
            record.extend(" ")
            record[2] = temp.Price["Price"]

            price = int(record[2].replace(',', ''))
            cursor.execute(
                "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Kosdaq_Afinance WHERE Code = %s AND Date like %s",
                (i["Code"], year + "%")
            )
            recent_data = cursor.fetchall()
            
            if (len(recent_data) is not 0):
                recent_data[0] = list(recent_data[0].values())
                if (recent_data[0][1] is "0" or recent_data[0][1] is "\xa0"):
                    year = str(int(year)-1)
                    cursor.execute(
                        "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Kosdaq_Afinance WHERE Code = %s AND Date like %s",
                        (i["Code"], year + "%")
                        )
                    recent_data2 = cursor.fetchall()
                    if (recent_data2[0][1] is "0" or recent_data2[0][1] is "\xa0"):
                        continue
                    recent_data2[0] = list(recent_data2[0].values())
                    recent_data[0] = recent_data2[0]
                    totalnum = int(recent_data2[0][1].replace(',', ''))
                else:
                    totalnum = int(recent_data[0][1].replace(',', ''))

                # PER
                record.extend(" ")
                if (recent_data[0][0] is not "\xa0"):
                    if (recent_data[0][0] is "0" or totalnum is 0):
                        continue
                    PER = float(price / float(
                        int(recent_data[0][0].replace(',', '')) * 100000 / totalnum))
                    record.extend(" ")
                    record[3] = str(round(PER, 2))

                # PBR
                record.extend(" ")
                if (recent_data[0][2] is not "\xa0" and recent_data[0][3] is not "\xa0"):
                    if (recent_data[0][2] is recent_data[0][3]):
                        continue
                    PBR = float(price / float((int(recent_data[0][2].replace(',', '')) - int(
                        recent_data[0][3].replace(',', ''))) * 100000 / totalnum))
                    record[4] = str(round(PBR, 2))

                # PSR
                record.extend(" ")
                if (recent_data[0][4] is not "\xa0"):
                    if (recent_data[0][4] is "0"):
                        continue
                    PSR = float(price / float(int(recent_data[0][4].replace(',', '')) * 100000 / totalnum))
                    record[5] = str(round(PSR, 2))

                print(record)
                kosdaq_record.extend(" ")
                kosdaq_record[len(kosdaq_record)-1] = record
                
                del (temp)
        for i in kosdaq_record:
            if len(i) == 6:
                cursor.execute("INSERT INTO Kosdaq_invest_info VALUES(%s,%s,%s,%s,%s,%s)", tuple(i))
            else:
                print("kosdaq :: worng format : " + i[0] + ", " + i[1])
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        
        for num,i in enumerate(konex):
            print("[{} / {}] {}".format(num,len(konex),i['Code']))
            temp = GF.StockFinance(i["Code"])
            temp.getPrice()

            record = [i["Name"], i["Code"]]
            record.extend(" ")
            record[2] = temp.Price["Price"]

            price = int(record[2].replace(',', ''))
            cursor.execute(
                "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Konex_Afinance WHERE Code = %s AND Date like %s",
                (i["Code"], year + "%")
            )
            recent_data = cursor.fetchall()
            if (len(recent_data) is not 0):
                recent_data[0] = list(recent_data[0].values())
                if (recent_data[0][1] is "0" or recent_data[0][1] is "\xa0"):
                    year = str(int(year)-1) 
                    cursor.execute(
                        "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Konex_Afinance WHERE Code = %s AND Date like %s",
                        (i["Code"], year + "%")
                    )
                    recent_data2 = cursor.fetchall()
                    if (recent_data2[0][1] is "0" or recent_data2[0][1] is "\xa0"):
                        continue
                    recent_data2[0] = list(recent_data2[0].values())
                    recent_data[0] = recent_data2[0]
                    totalnum = int(recent_data2[0][1].replace(',', ''))
                else:
                    totalnum = int(recent_data[0][1].replace(',', ''))
                    
                # PER
                record.extend(" ")
                if (recent_data[0][0] is not "\xa0"):
                    if (recent_data[0][0] is "0" or totalnum is 0):
                        continue
                    PER = float(price / float(int(recent_data[0][0].replace(',', '')) * 100000 / totalnum))
                    record[3] = str(round(PER, 2))

                # PBR
                record.extend(" ")
                if (recent_data[0][2] is not "\xa0" and recent_data[0][3] is not "\xa0"):
                    if (recent_data[0][2] is recent_data[0][3]):
                        continue
                    PBR = float(price / float((int(recent_data[0][2].replace(',', '')) - int(
                        recent_data[0][3].replace(',', ''))) * 100000 / totalnum))
                    record[4] = str(round(PBR, 2))

                # PSR
                record.extend(" ")
                if (recent_data[0][4] is not "\xa0"):
                    if (recent_data[0][4] is "0"):
                        continue
                    PSR = float(price / float(int(recent_data[0][4].replace(',', '')) * 100000 / totalnum))
                    record[5] = str(round(PSR, 2))

                print(record)
                konex_record.extend(" ")
                konex_record[len(konex_record)-1] = record
                
                del (temp)
        for i in konex_record:
            if len(i) == 6:
                cursor.execute("INSERT INTO Konex_invest_info VALUES(%s,%s,%s,%s,%s,%s)", tuple(i))
            else:
                print("konex :: worng format : " + i[0] + ", " + i[1])
        con.commit()
    con.close()


def Insert_DB_exp_invest(parayear,sector):
    kospi = Get_DB_info("Kospi_info")
    kosdaq = Get_DB_info("Kosdaq_info")
    konex = Get_DB_info("Konex_info")

    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    totalnum = 0

    year = str(parayear)

    kospi_record = []
    kosdaq_record = []
    konex_record = []

    count = 0
    if(sector % 2 is 1):
        for i in kospi:
            print(i['Code'])
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
            if (len(recent_data) is not 0):
                if (recent_data[0][1] is "0" or recent_data[0][1] is "\xa0"):
                    year =  str(int(year) - 1) #추후에 year값도 저장
                    cursor.execute(
                        "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Kospi_Afinance WHERE Code = %s AND Date like %s",
                        (i['Code'], year + "%")
                        )
                    recent_data2 = cursor.fetchall()
                    if (recent_data2[0][1] is "0" or recent_data2[0][1] is "\xa0"):
                        continue
                    totalnum = int(recent_data2[0][1].replace(',', ''))
                else:
                    totalnum = int(recent_data[0][1].replace(',', ''))

                # PER
                record.extend(" ")
                if (recent_data[0][0] is not "\xa0"):
                    if (recent_data[0][0] is "0" or totalnum is 0):
                        continue
                    PER = float(price / float(int(recent_data[0][0].replace(',', '')) * 100000 / totalnum))
                    record[3] = str(round(PER, 2))

                # PBR
                record.extend(" ")
                if (recent_data[0][2] is not "\xa0" and recent_data[0][3] is not "\xa0"):
                    if (recent_data[0][2] is recent_data[0][3]):
                        continue
                    PBR = float(price / float((int(recent_data[0][2].replace(',', '')) - int(
                        recent_data[0][3].replace(',', ''))) * 100000 / totalnum))
                    record[4] = str(round(PBR, 2))

                # PSR
                record.extend(" ")
                if (recent_data[0][4] is not "\xa0"):
                    if (recent_data[0][4] is "0"):
                        continue
                    PSR = float(price / float(int(recent_data[0][4].replace(',', '')) * 100000 / totalnum))
                    record[5] = str(round(PSR, 2))

                print(record)
                kospi_record.extend(" ")
                kospi_record[len(kospi_record)-1] = record
                #count += 1
                del (temp)
                
        for i in kospi_record:
            if len(i) == 6:
                cursor.execute("INSERT INTO Kospi_invest_info VALUES(%s,%s,%s,%s,%s,%s)", tuple(i))
            else:
                print("kospi :: worng format : " + i[0] + ", " + i[1])
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        count = 0
        for i in kosdaq:
            print(i['Code'])
            temp = GF.StockFinance(i['Code'])
            temp.getPrice()
            
            # if(count is 5):            테스트용
            #     break
            
            record = [i['Name'], i['Code']]
            record.extend(" ")
            record[2] = temp.Price["Price"]

            price = int(record[2].replace(',', ''))
            cursor.execute(
                "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Kosdaq_Afinance WHERE Code = %s AND Date like %s",
                (i[1], year + "%")
            )
            recent_data = cursor.fetchall()
            if (len(recent_data) is not 0):
                if (recent_data[0][1] is "0" or recent_data[0][1] is "\xa0"):
                    year = str(int(year)-1)
                    cursor.execute(
                        "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Kosdaq_Afinance WHERE Code = %s AND Date like %s",
                        (i[1], year + "%")
                        )
                    recent_data2 = cursor.fetchall()
                    if (recent_data2[0][1] is "0" or recent_data2[0][1] is "\xa0"):
                        continue
                    totalnum = int(recent_data2[0][1].replace(',', ''))
                else:
                    totalnum = int(recent_data[0][1].replace(',', ''))

                # PER
                record.extend(" ")
                if (recent_data[0][0] is not "\xa0"):
                    if (recent_data[0][0] is "0" or totalnum is 0):
                        continue
                    PER = float(price / float(
                        int(recent_data[0][0].replace(',', '')) * 100000 / totalnum))
                    record.extend(" ")
                    record[3] = str(round(PER, 2))

                # PBR
                record.extend(" ")
                if (recent_data[0][2] is not "\xa0" and recent_data[0][3] is not "\xa0"):
                    if (recent_data[0][2] is recent_data[0][3]):
                        continue
                    PBR = float(price / float((int(recent_data[0][2].replace(',', '')) - int(
                        recent_data[0][3].replace(',', ''))) * 100000 / totalnum))
                    record[4] = str(round(PBR, 2))

                # PSR
                record.extend(" ")
                if (recent_data[0][4] is not "\xa0"):
                    if (recent_data[0][4] is "0"):
                        continue
                    PSR = float(price / float(int(recent_data[0][4].replace(',', '')) * 100000 / totalnum))
                    record[5] = str(round(PSR, 2))

                print(record)
                kosdaq_record.extend(" ")
                kosdaq_record[len(kosdaq_record)-1] = record
                #count += 1
                del (temp)
        for i in kosdaq_record:
            if len(i) == 6:
                cursor.execute("INSERT INTO Kosdaq_invest_info VALUES(%s,%s,%s,%s,%s,%s)", tuple(i))
            else:
                print("kosdaq :: worng format : " + i[0] + ", " + i[1])
        con.commit()

    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        count = 0
        for i in konex:
            print(i["Code"])
            temp = GF.StockFinance(i["Code"])
            temp.getPrice()

            record = [i["Name"], i["Code"]]
            record.extend(" ")
            record[2] = temp.Price["Price"]

            price = int(record[2].replace(',', ''))
            cursor.execute(
                "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Konex_Afinance WHERE Code = %s AND Date like %s",
                (i["Code"], year + "%")
            )
            recent_data = cursor.fetchall()
            if (len(recent_data) is not 0):
                if (recent_data[0][1] is "0" or recent_data[0][1] is "\xa0"):
                    year = str(int(year)-1) 
                    cursor.execute(
                        "SELECT NetIncome, NumOutstandingShares,TotalAsset, TotalDebt,SalesAccount FROM Konex_Afinance WHERE Code = %s AND Date like %s",
                        (i[1], year + "%")
                    )
                    recent_data2 = cursor.fetchall()
                    if (recent_data2[0][1] is "0" or recent_data2[0][1] is "\xa0"):
                        continue
                    totalnum = int(recent_data2[0][1].replace(',', ''))
                else:
                    totalnum = int(recent_data[0][1].replace(',', ''))
                    
                # PER
                record.extend(" ")
                if (recent_data[0][0] is not "\xa0"):
                    if (recent_data[0][0] is "0" or totalnum is 0):
                        continue
                    PER = float(price / float(int(recent_data[0][0].replace(',', '')) * 100000 / totalnum))
                    record[3] = str(round(PER, 2))

                # PBR
                record.extend(" ")
                if (recent_data[0][2] is not "\xa0" and recent_data[0][3] is not "\xa0"):
                    if (recent_data[0][2] is recent_data[0][3]):
                        continue
                    PBR = float(price / float((int(recent_data[0][2].replace(',', '')) - int(
                        recent_data[0][3].replace(',', ''))) * 100000 / totalnum))
                    record[4] = str(round(PBR, 2))

                # PSR
                record.extend(" ")
                if (recent_data[0][4] is not "\xa0"):
                    if (recent_data[0][4] is "0"):
                        continue
                    PSR = float(price / float(int(recent_data[0][4].replace(',', '')) * 100000 / totalnum))
                    record[5] = str(round(PSR, 2))

                print(record)
                konex_record.extend(" ")
                konex_record[len(konex_record)-1] = record
                #count += 1
                del (temp)
        for i in konex_record:
            if len(i) == 6:
                cursor.execute("INSERT INTO Konex_invest_info VALUES(%s,%s,%s,%s,%s,%s)", tuple(i))
            else:
                print("konex :: worng format : " + i[0] + ", " + i[1])
        con.commit()
    con.close()


if __name__ == "__main__":
    #Reset_DB()
    # Create_DB()
    # Insert_DB_info()
    #Insert_DB_Afinance(KOSDAQ)
    Insert_DB_invest(2019,KOSDAQ)
    #Insert_DB_exp_invest(2019, KOSDAQ)



