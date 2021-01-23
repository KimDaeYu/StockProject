import pandas
import pymysql
import sys
import os
from DB_setting import *



def Get_invest_csv(sector = 7, expect = 'P', date = 2020):
    con = Connect_DB()
    path = str(os.path.abspath(__file__))[:-23] + "execl/" + str(date) + '_'
    if (sector % 2 == 1):
        sql="select * from "
        if(expect == "E"):
            filename = "kospi_exp_invest.csv"
            table = r"Kospi_exp_invest_info"
            result = pandas.read_sql_query(sql+table,con)
            result.to_csv(path+filename,index=False)
        else:
            filename = "kospi_invest.csv"
            table = "Kospi_qinvest_info"
            result = pandas.read_sql_query(sql+table,con)
            result.to_csv(path+filename,index=False)
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        sql="select * from "
        if(expect == "E"):
            filename = "kosdaq_exp_invest.csv"
            table = "Kosdaq_exp_invest_info"
            result = pandas.read_sql_query(sql+table,con)
            result.to_csv(path+filename,index=False)
        else:
            filename = "kosdaq_invest.csv"
            table = "Kosdaq_invest_info"
            result = pandas.read_sql_query(sql+table,con)
            result.to_csv(path+filename,index=False)
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        sql="select * from "
        if(expect == "E"):
            filename = "konex_exp_invest.csv"
            table = "Konex_exp_invest_info"
            result = pandas.read_sql_query(sql+table,con)
            result.to_csv(path+filename,index=False)
        else:
            filename = "konex_invest.csv"
            table = "Konex_invest_info"
            result = pandas.read_sql_query(sql+table,con)
            result.to_csv(path+filename,index=False)
    con.close()

if __name__ == "__main__":
    if(len(sys.argv) == 0):
        print("plese set three argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4 / P, E/ data_name ex)20200831")
    elif(len(sys.argv) == 4):
        Get_invest_csv(int(sys.argv[1]),sys.argv[2],sys.argv[3])
    else:
        print("plese set three argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4 / P, E / data_name ex)20200831")