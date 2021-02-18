import pandas
import pymysql
import sys
import os

sys.path.append("..")
from DB_setting import *



def Get_invest_csv(term = 'Q', sector = 7, date = 2020):
    con = Connect_DB()
    path = str(os.path.abspath(__file__))[:-27] + "execl/" + str(date) + '_'
    if (sector % 2 == 1):
        sql="select * from "
        if(term == "Q"):
            filename = "kospi_Qinvest.csv"
            table = "Kospi_Qinvest_info"
            result = pandas.read_sql_query(sql+table,con)
            result.to_csv(path+filename,index=False)
        else:
            filename = "kospi_Ainvest.csv"
            table = "Kospi_Ainvest_info"
            result = pandas.read_sql_query(sql+table,con)
            result.to_csv(path+filename,index=False)
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        sql="select * from "
        if(term == "Q"):
            filename = "kosdaq_Qinvest.csv"
            table = "Kosdaq_Qinvest_info"
            result = pandas.read_sql_query(sql+table,con)
            result.to_csv(path+filename,index=False)
        else:
            filename = "kosdaq_Ainvest.csv"
            table = "Kosdaq_Ainvest_info"
            result = pandas.read_sql_query(sql+table,con)
            result.to_csv(path+filename,index=False)
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        sql="select * from "
        if(term == "Q"):
            filename = "konex_Qinvest.csv"
            table = "Konex_Qinvest_info"
            result = pandas.read_sql_query(sql+table,con)
            result.to_csv(path+filename,index=False)
        else:
            filename = "konex_Ainvest.csv"
            table = "Konex_Ainvest_info"
            result = pandas.read_sql_query(sql+table,con)
            result.to_csv(path+filename,index=False)
    con.close()

if __name__ == "__main__":
    if(len(sys.argv) == 0):
        print("plese set three argument :: Annual(A), Quarter(Q) / kospi -> 1 + kosdaq -> 2 + konex -> 4 / data_name ex)20200831")
    elif(len(sys.argv) == 4):
        Get_invest_csv(sys.argv[1],int(sys.argv[2]),sys.argv[3])
    else:
        print("plese set three argument :: Annual(A), Quarter(Q) / kospi -> 1 + kosdaq -> 2 + konex -> 4 / data_name ex)20200831")