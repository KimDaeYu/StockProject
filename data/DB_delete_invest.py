import sys

import pymysql
from DB_setting import *

KOSPI = 1
KOSDAQ = 2
KONEX = 4

def Reset_invest_DB(sector, expect):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    if(sector % 2 == 1):
        if(expect == "E"):
            cursor.execute("DELETE FROM Kospi_exp_invest_info;")
            con.commit()
        else:
            cursor.execute("DELETE FROM Kospi_invest_info;")
            con.commit()
    sector /= 2
    sector = int(sector)
    if(sector % 2 == 1):
        if(expect == "E"):
            cursor.execute("DELETE FROM Kosdaq_exp_invest_info;")
            con.commit()
        else:
            cursor.execute("DELETE FROM Kosdaq_invest_info;")
            con.commit()
    sector /= 2
    sector = int(sector)
    if(sector % 2 == 1):
        if(expect == "E"):
            cursor.execute("DELETE FROM Konex_exp_invest_info;")
            con.commit()
        else:
            cursor.execute("DELETE FROM Konex_invest_info;")
            con.commit()
    con.close()


if __name__ == "__main__":
    if(len(sys.argv) == 0):
        print("plese set two argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4 / P, E")
    elif(len(sys.argv) == 3):
        Reset_invest_DB(int(sys.argv[1]), sys.argv[2])
    else:
        print("plese set two argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4 / P, E")



