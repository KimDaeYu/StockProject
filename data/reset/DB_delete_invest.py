import sys

import pymysql
from DB_setting import *

KOSPI = 1
KOSDAQ = 2
KONEX = 4

def Reset_invest_DB(term, sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    if(sector % 2 == 1):
        if(term == "Q"):
            cursor.execute("DELETE FROM Kospi_Qinvest_info;")
            con.commit()
        else:
            cursor.execute("DELETE FROM Kospi_Ainvest_info;")
            con.commit()
    sector /= 2
    sector = int(sector)
    if(sector % 2 == 1):
        if(term == "Q"):
            cursor.execute("DELETE FROM Kosdaq_Qinvest_info;")
            con.commit()
        else:
            cursor.execute("DELETE FROM Kosdaq_Ainvest_info;")
            con.commit()
    sector /= 2
    sector = int(sector)
    if(sector % 2 == 1):
        if(term == "Q"):
            cursor.execute("DELETE FROM Konex_Qinvest_info;")
            con.commit()
        else:
            cursor.execute("DELETE FROM Konex_Ainvest_info;")
            con.commit()
    con.close()


if __name__ == "__main__":
    if(len(sys.argv) == 0):
        print("plese set two argument :: Annual(A), Quarter(Q) / kospi -> 1 + kosdaq -> 2 + konex -> 4")
    elif(len(sys.argv) == 3):
        Reset_invest_DB(int(sys.argv[1]), sys.argv[2])
    else:
        print("plese set two argument :: Annual(A), Quarter(Q) / kospi -> 1 + kosdaq -> 2 + konex -> 4")


