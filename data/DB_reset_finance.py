import sys

import pymysql
from DB_setting import *

KOSPI = 1
KOSDAQ = 2
KONEX = 4

def Reset_DB(sector, term):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    if (sector % 2 == 1):
        if(term == 0):    #0 : 연간, 1 : 분기간
            cursor.execute("""
            DROP TABLE IF EXISTS Kospi_Afinance;
            """)
        else:
            cursor.execute("""
            DROP TABLE IF EXISTS Kospi_Qfinance;
            """)
        con.commit()
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        if(term == 0):    #0 : 연간, 1 : 분기간
            cursor.execute("""
            DROP TABLE IF EXISTS Kosdaq_Afinance;
            """)
        else:
            cursor.execute("""
            DROP TABLE IF EXISTS Kosdaq_Qfinance;
            """)
        con.commit()
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        if(term == 0):    #0 : 연간, 1 : 분기간
            cursor.execute("""
            DROP TABLE IF EXISTS Konex_Afinance;
            """)
        else:
            cursor.execute("""
            DROP TABLE IF EXISTS Konex_Qfinance;
            """)
        con.commit()
    con.close()
    
    
def Create_DB(sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    if (sector % 2 == 1):
        if(term == 0):    #0 : 연간, 1 : 분기간
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
            `DividendYieldRatio`	TEXT
                );""")
        else:
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
            `DividendYieldRatio`	TEXT
             );""")
        con.commit()
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        if(term == 0):    #0 : 연간, 1 : 분기간
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
            `DividendYieldRatio`	TEXT
                );""")
        else:
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
            `DividendYieldRatio`	TEXT
             );""")
        con.commit()
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        if(term == 0):    #0 : 연간, 1 : 분기간
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
            `DividendYieldRatio`	TEXT
                );""")
        else:
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
            `DividendYieldRatio`	TEXT
             );""")
        con.commit()
    con.close()


if __name__ == "__main__":
    if(len(sys.argv) == 0):
        print("plese set two argument :: Annual(A), Quarter(Q) / kospi -> 1 + kosdaq -> 2 + konex -> 4")
    elif(len(sys.argv) == 3):
        if(sys.argv[1] == 'A' or sys.argv[1] == 'Annual'):
            Reset_DB(int(sys.argv[1]),0)
            Create_DB(int(sys.argv[1]),0)
        if(sys.argv[1] == 'Q' or sys.argv[1] == 'Quarter'):
            Reset_DB(int(sys.argv[1]),1)
            Create_DB(int(sys.argv[1]),1)
    else:
        print("plese set two argument :: Annual(A), Quarter(Q) / kospi -> 1 + kosdaq -> 2 + konex -> 4")

