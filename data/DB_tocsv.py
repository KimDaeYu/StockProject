import sys
import os
import shutil

import pymysql
from DB_setting import *

KOSPI = 1
KOSDAQ = 2
KONEX = 4

def Get_invest_csv(sector,expect, date = 0):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    path = str(os.path.abspath(__file__))[:-16] + "execl/" + str(date) + '_'
    if (sector % 2 == 1):
        if(expect == "E"):
            filename = "kospi_invest.csv"
            table = "Kospi_exp_invest_info"
            cursor.execute("""
               SELECT * INTO OUTFILE %s FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\\\' LINES TERMINATED BY '\\n' FROM """ + table + """;
              """, [filename])
            con.commit()
            shutil.copy("/var/lib/mysql/" + Get_DB() + "/" + filename,  path + filename)
            file = '/var/lib/mysql/study_db/' + filename
            if os.path.isfile(file):
                os.remove(file)
        else:
            filename = "kospi_invest.csv"
            table = "Kospi_invest_info"
            cursor.execute("""
               SELECT * INTO OUTFILE %s FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\\\' LINES TERMINATED BY '\\n' FROM """ + table + """;
              """, [filename])
            con.commit()
            shutil.copy("/var/lib/mysql/" + Get_DB() + "/" + filename, path + filename)
            file = '/var/lib/mysql/study_db/' + filename
            if os.path.isfile(file):
                os.remove(file)

    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        if(expect == "E"):
            filename = "kosdaq_invest.csv"
            table = "Kosdaq_exp_invest_info"
            cursor.execute("""
               SELECT * INTO OUTFILE %s FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\\\' LINES TERMINATED BY '\\n' FROM """ + table + """;
              """, [filename])
            shutil.copy("/var/lib/mysql/" + Get_DB() + "/" + filename,path + filename)
            file = '/var/lib/mysql/study_db/' + filename
            if os.path.isfile(file):
                os.remove(file)
        else:
            filename = "kosdaq_invest.csv"
            table = "Kosdaq_invest_info"
            cursor.execute("""
               SELECT * INTO OUTFILE %s FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\\\' LINES TERMINATED BY '\\n' FROM """ + table + """;
              """, [filename])
            shutil.copy("/var/lib/mysql/" + Get_DB() + "/" + filename, path + filename)
            file = '/var/lib/mysql/study_db/' + filename
            if os.path.isfile(file):
                os.remove(file)
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        if(expect == "E"):
            filename = "konex_invest.csv"
            table = "Konex_exp_invest_info"
            cursor.execute("""
               SELECT * INTO OUTFILE %s FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\\\' LINES TERMINATED BY '\\n' FROM """ + table + """;
              """, [filename])
            shutil.copy("/var/lib/mysql/" + Get_DB() + "/" + filename, path + filename)
            file = '/var/lib/mysql/study_db/' + filename
            if os.path.isfile(file):
                os.remove(file)
        else:
            filename = "konex_invest.csv"
            table = "Konex_invest_info"
            cursor.execute("""
               SELECT * INTO OUTFILE %s FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\\\' LINES TERMINATED BY '\\n' FROM """ + table + """;
              """, [filename])
            shutil.copy("/var/lib/mysql/" + Get_DB() + "/" + filename,path + filename)
            file = '/var/lib/mysql/study_db/' + filename
            if os.path.isfile(file):
                os.remove(file)
    con.close()


if __name__ == "__main__":
    if(len(sys.argv) == 0):
        print("plese set three argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4 / P, E/ data_name ex)20200831")
    elif(len(sys.argv) == 4):
        Get_invest_csv(int(sys.argv[1]),sys.argv[2],sys.argv[3])
    else:
        print("plese set three argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4 / P, E / data_name ex)20200831")
        



