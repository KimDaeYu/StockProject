import sys

import pymysql
from DB_setting import *

KOSPI = 1
KOSDAQ = 2
KONEX = 4

def Reset_invest_DB(sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    if (sector % 2 == 1):
        cursor.execute("""
        DROP TABLE IF EXISTS Kospi_invest_info;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Kospi_exp_invest_info;
          """)
        con.commit()
        
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        cursor.execute("""
        DROP TABLE IF EXISTS Kosdaq_invest_info;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Kosdaq_exp_invest_info;
          """)
        con.commit()
    
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        cursor.execute("""
        DROP TABLE IF EXISTS Konex_invest_info;
          """)
        cursor.execute("""
        DROP TABLE IF EXISTS Konex_exp_invest_info;
          """)
        con.commit()
    con.close()
    
    
def Create_invest_DB(sector):
    con = Connect_DB()
    cursor = con.cursor(pymysql.cursors.DictCursor)
    if (sector % 2 == 1):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kospi_invest_info` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Price`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `PSR`	TEXT,
        `Year`  TEXT
           );  """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kospi_exp_invest_info` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Price`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `PSR`	TEXT,
        `Year`  TEXT
            );  """)
        con.commit()
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kosdaq_invest_info` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Price`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `PSR`	TEXT,
        `Year`  TEXT
         ); """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Kosdaq_exp_invest_info` (
        `Name`	VARCHAR(25) NOT NULL,
         `Code`	VARCHAR(10) NOT NULL,
        `Price`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `PSR`	TEXT,
        `Year`  TEXT
          ); """)
        con.commit()
    sector /= 2
    sector = int(sector)
    if (sector % 2 == 1):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Konex_invest_info` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Price`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `PSR`	TEXT,
        `Year`  TEXT
         ); """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Konex_exp_invest_info` (
        `Name`	VARCHAR(25) NOT NULL,
        `Code`	VARCHAR(10) NOT NULL,
        `Price`	TEXT,
        `PER`	TEXT,
        `PBR`	TEXT,
        `PSR`	TEXT,
        `Year`  TEXT
         ); """)
        con.commit()
    con.close()


if __name__ == "__main__":
    if(len(sys.argv) == 0):
        print("plese set one argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4")
    elif(len(sys.argv) == 2):
        Reset_invest_DB(int(sys.argv[1]))
        Create_invest_DB(int(sys.argv[1]))
    else:
        print("plese set one argument :: kospi -> 1 + kosdaq -> 2 + konex -> 4")
        



