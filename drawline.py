import sqlite3
import pyimgur
from matplotlib import use
import requests
import pandas as pd
import numpy as np
import datetime,time,re
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression
from pandas.core.frame import DataFrame

#imgur
#client ID:9fa3e553d6f1121
#client secret:548effd3aa72429d50ae27b21ee642e8845d9d68

def linebot_draw_fiveline(msg):
    conn = sqlite3.connect('C:/Users/User/Desktop/FinTech/ETF_linebot/fund_data.db')
    cursor = conn.cursor()
    sql =f"select * from Strategy_data where Number = '{msg}'"
    cursor.execute(sql)
    data = cursor.fetchall()

    Net_worth = []
    P2SD= []
    P1SD = []
    TL = []
    N2SD = []
    N1SD = []
    for row in data:
        #date.append(row[0])
        Net_worth.append(row[2])
        P2SD.append(row[3])
        P1SD.append(row[4])
        TL.append(row[5])
        N2SD.append(row[6])
        N1SD.append(row[7])
    plt.figure(facecolor = 'white', figsize = (9,3), dpi=100)
    plt.plot(Net_worth)
    plt.plot(P2SD)
    plt.plot(P1SD)
    plt.plot(TL)
    plt.plot(N2SD)
    plt.plot(N1SD)
    plt.title(f"{msg}.TW", color = 'black', fontsize = 24) 
    plt.ylabel("Stock price")
    plt.savefig(f'FIVELINE{msg}.png')
    plt.plot

    CLIENT_ID = "9fa3e553d6f1121"
    PATH = f"FIVELINE{msg}.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=f"FIVELINE{msg}")
    return uploaded_image.link

def linebot_draw_fivelinebb(msg):
    conn = sqlite3.connect('C:/Users/User/Desktop/FinTech/ETF_linebot/fund_data.db')
    cursor = conn.cursor()
    sql =f"select * from Strategy_data where Number = '{msg}'"
    cursor.execute(sql)
    data = cursor.fetchall()

    date = []
    Net_worth = []
    bbh = []
    bbm = []
    bbl = []
    for row in data:
        date.append(row[0])
        Net_worth.append(row[2])
        bbh.append(row[8])
        bbm.append(row[9])
        bbl.append(row[10])

    plt.figure(facecolor = 'white', figsize = (15,5), dpi=100)
    plt.plot(date, Net_worth)
    plt.plot(date, bbh)
    plt.plot(date, bbm)
    plt.plot(date, bbl)
    plt.title(f"{msg}.TW", color = 'black', fontsize = 24) 
    plt.ylabel("Stock price")
    plt.savefig(f'FivelineBB{msg}.png')
    plt.plot

    CLIENT_ID = "9fa3e553d6f1121"
    PATH = f"FivelineBB{msg}.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=f"FivelineBB{msg}")
    return uploaded_image.link