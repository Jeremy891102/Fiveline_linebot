import sqlite3, time
from pandas.io import sql
import requests
import pandas as pd
import numpy as np
import datetime,time,re
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression
today = datetime.date.today()
end = today - datetime.timedelta(days=1)
start = end - datetime.timedelta(days=365*3.5)

def get_sql2():
    conn = sqlite3.connect('C:/Users/User/Desktop/FinTech/ETF_linebot/fund_data.db')
    cursor = conn.cursor()
    sql = "select Quote_change from fund_data where Date = ? and FundID = ?"
    cursor.execute(sql, ('2022-12-20', 'F0HKG05WWU:FO'))
    rows = cursor.fetchall()
    return rows

def basic_information(msg):
    conn = sqlite3.connect('C:/Users/User/Desktop/FinTech/ETF_linebot/fund_data.db')
    cursor = conn.cursor()
    sql = f"select * from fund_data where FundID = '{msg}'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    newList = list(reversed(rows))
    content = (f'FundID: {newList[0][0]}\nDate: {newList[0][1]}\nNet_worth: {newList[0][2]}\nUp_down: {newList[0][3]}\nQuote_change: {newList[0][4]}\n')
    return content

