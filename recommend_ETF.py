import os
import sqlite3
from pathlib import Path
import datetime
import pandas as pd
import numpy as np
import datetime,time,re
from sklearn.linear_model import LinearRegression
import requests
from bs4 import BeautifulSoup

today = datetime.date.today()
end = today - datetime.timedelta(days=1)
start = end - datetime.timedelta(days=365*3.5)

dict_from_ETF_list= pd.read_excel("C:/Users/User/Desktop/LineBot/FiveLineAPP/ETF_list.xlsx")
ETF_list = dict_from_ETF_list['Number']

def five_line (data):
    timetrend = list(range(1, data.shape[0]+1))
    data['Date'] = timetrend
    data = data[['Date','Net_worth']]
    data = data.dropna()
    reg = LinearRegression()
    x = data['Date'].to_frame ()
    y = data['Net_worth'].to_frame ()
    reg.fit(x,y)
    a = reg.intercept_
    beta = reg.coef_
    longtrend = a + beta*x
    print(longtrend)
    res = np.array(list(data['Net_worth'])) - np.array(list(longtrend['Date']))
    std = np.std(res, ddof=1) #residual std
    fiveline = pd.DataFrame ()
    fiveline['+2SD'] = longtrend['Date'] + (2*std)
    fiveline['+1SD'] = longtrend['Date'] + (1*std)
    fiveline['TL'] = longtrend['Date']
    fiveline['-1SD'] = longtrend['Date'] - (1*std)
    fiveline['-2SD'] = longtrend['Date'] - (2*std)
    use_fiveline = pd.merge(data,fiveline[['+2SD', '+1SD', 'TL', '-1SD', '-2SD']], left_index=True, right_index=True, how='left')
    pick_fiveline = use_fiveline[['Net_worth','+2SD', '+1SD', 'TL', '-1SD', '-2SD']]
    return pick_fiveline,beta

def stock_price(stock:str):

    data = requests.get(f"https://tw.stock.yahoo.com/fund/history/{stock}")
    soup = BeautifulSoup(data.text)
    price = soup.find('span',{'class':'Fz(40px) Fw(b) Lh(1) C($c-primary-text)'})
    return price.text



def recommend(recommend_count):
    recommend = recommend_count
    recommended = 0 
    reply = ''
    df= pd.read_csv("C:/Users/User/Desktop/FinTech/ETF_linebot/chosen.csv")
    df.columns=["index","Number"]
    chosen=df["Number"]
    for i in chosen:
        reply += '基金代碼:\n' + i +'\n已低於兩個標準差，建議買進!!\n'
        recommended += 1
        if recommended == recommend:
            break
        else:continue
            #return reply
        if reply == '':
            return 'none'
    return reply