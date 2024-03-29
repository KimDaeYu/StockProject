import sys

import pymysql
from DB_setting import *
from DB_reset import *


KOSPI = 1
KOSDAQ = 2
KONEX = 4

def Reset_invest_DB(sector,term):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    if (sector % 2 == 1):
        if(term == 0):    #0 : 연간, 1 : 분기간
            cursor.execute("""
            DROP TABLE IF EXISTS Kospi_Ainvest_info;
              """)
        else:
            cursor.execute("""
            DROP TABLE IF EXISTS Kospi_Qinvest_info;
            """)
        con.commit()
        
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        if(term == 0):    #0 : 연간, 1 : 분기간
            cursor.execute("""
            DROP TABLE IF EXISTS Kosdaq_Ainvest_info;
              """)
        else:
            cursor.execute("""
            DROP TABLE IF EXISTS Kosdaq_Qinvest_info;
            """)
        con.commit()
    
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        if(term == 0):    #0 : 연간, 1 : 분기간
            cursor.execute("""
            DROP TABLE IF EXISTS Konex_Ainvest_info;
              """)
        else:
            cursor.execute("""
            DROP TABLE IF EXISTS Konex_Qinvest_info;
            """)
        con.commit()
    con.close()
    
#`mod_date` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
def Create_invest_DB(sector):
    if (sector % 2 == 1):
        Create_DB(1)
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        Create_DB(2)
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        Create_DB(4)


if __name__ == "__main__":
    if(len(sys.argv) == 0):
        print("plese set two argument :: Annual(A), Quarter(Q) / kospi -> 1 + kosdaq -> 2 + konex -> 4")
    elif(len(sys.argv) == 3):
        if(sys.argv[1] == 'A' or sys.argv[1] == 'Annual'):
            Reset_invest_DB(int(sys.argv[2]),0)
        if(sys.argv[1] == 'Q' or sys.argv[1] == 'Quarter'):
            Reset_invest_DB(int(sys.argv[2]),1)
        Create_invest_DB(int(sys.argv[2]))
    else:
        print("plese set two argument :: Annual(A), Quarter(Q) / kospi -> 1 + kosdaq -> 2 + konex -> 4")


