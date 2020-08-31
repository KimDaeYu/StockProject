import sys
import os
import shutil

import pymysql
from DB_setting import *

KOSPI = 1
KOSDAQ = 2
KONEX = 4

def Get_invest_csv(sector, date = 0):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    if (sector % 2 is 1):
        filename = "kospi_invest.csv"
        table = "Kospi_invest_info"
        cursor.execute("""
           SELECT * INTO OUTFILE %s FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\\\' LINES TERMINATED BY '\\n' FROM """ + table + """;
          """, [filename])
        con.commit()
        shutil.copy("/var/lib/mysql/" + Get_DB() + "/" + filename,                                         "/workspace/StockProject2/execl/" + str(date) + '_' + filename)
        file = '/var/lib/mysql/study_db/' + filename
        if os.path.isfile(file):
            os.remove(file)

    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        filename = "kosdaq_invest.csv"
        table = "Kosdaq_invest_info"
        cursor.execute("""
           SELECT * INTO OUTFILE %s FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\\\' LINES TERMINATED BY '\\n' FROM """ + table + """;
          """, [filename])
        shutil.copy("/var/lib/mysql/" + Get_DB() + "/" + filename,                                         "/workspace/StockProject2/execl/" + str(date) + '_' + filename)
        file = '/var/lib/mysql/study_db/' + filename
        if os.path.isfile(file):
            os.remove(file)
    sector /= 2
    sector = int(sector)
    if (sector % 2 is 1):
        filename = "konex_invest.csv"
        table = "Konex_invest_info"
        cursor.execute("""
           SELECT * INTO OUTFILE %s FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\\\' LINES TERMINATED BY '\\n' FROM """ + table + """;
          """, [filename])
        shutil.copy("/var/lib/mysql/" + Get_DB() + "/" + filename,                                         "/workspace/StockProject2/execl/" + str(date) + '_' + filename)
        file = '/var/lib/mysql/study_db/' + filename
        if os.path.isfile(file):
            os.remove(file)
    con.close()


if __name__ == "__main__":
    if(len(sys.argv) == 0):
        print("plese set two argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4 / data ex)20200831")
    elif(len(sys.argv) == 3):
        Get_invest_csv(int(sys.argv[1]),sys.argv[2])
    else:
        print("plese set two argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4 / data ex)20200831")
        



