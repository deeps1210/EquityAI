# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 16:34:37 2019

@author: sunil
"""

#from nsepy import get_history
#sbin = get_history(symbol='SBIN',
#                   start=date(2017,1,1),
#                   end=date(2019,4,1))




#from nsetools import Nse
#from pprint import pprint
import mysql.connector
from datetime import date
from datetime import timedelta
import pandas as pd

#import sys
#import json
from nsepy.history import get_price_list
#import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:admin@localhost:3306/nsetrading', echo=False)

#ta-lib library for analysis


holidaydf = pd.read_excel('HolidayList.xlsx', sheet_name='Sheet1')
holidaylist=[item.date() for item in holidaydf['Date'].tolist()]

MYSQL_HOST="localhost"
MYSQL_USER="root"
MYSQL_PWD="admin"
MYSQL_DATABASE="nsetrading"


try:
    # Load the configuratoin externally from config
    mydbconn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd="admin",
            database=MYSQL_DATABASE,
            auth_plugin="mysql_native_password"
            )

    start_date = date(2012,1,1)
    end_date = date(2012,1,1)
    
    #prices = get_price_list(start_date)
    
    day_count = (end_date - start_date).days + 1
    one_day=timedelta(1,0,0)
    for dayloop in range(0,day_count,1):
        tradingdate = start_date + timedelta(dayloop,0,0)
        print()
        if(tradingdate in holidaylist or tradingdate.weekday() in (5,6)):
            continue
        print('trading date ->', tradingdate)
        prices = get_price_list(tradingdate)
        #prices.to_sql(con=mydbconn, name='stock_price_history', if_exists='replace', flavor='mysql')
        prices.to_sql('stock_price_hist', con=engine, if_exists='append')
        mydbconn.commit()
        print ("Record inserted successfully into python_users table")
    
    #    mycursor = mydbconn.cursor()
    #    sql_insert_query = "INSERT INTO  stockdaily_raw(nse_symbol,load_datetime,stock_rawdata) VALUES (%s,%s,%s)"
    #    val1='INFY'
    #    insert_tuple = (val1)
    #    for stock_row_string in stock_rawdata:
    #        json_stock_row = json.loads(stock_row_string);
    #        result  = mycursor.execute(sql_insert_query, (json_stock_row['symbol'] ,currdatetime, stock_row_string))

except mysql.connector.Error as error :
    mydbconn.rollback()
    print("Failed to insert into MySQL table {}".format(error))
except BadZipfile as error:
    print("Does not work ")
finally:
    #closing database connection.
    if(mydbconn.is_connected()):
        mydbconn.close()
        print("MySQL connection is closed")
        