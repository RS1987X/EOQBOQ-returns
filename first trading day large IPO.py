# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 15:50:47 2021

@author: richa
"""


import yfinance as yf
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


#download data for biggest IPOs last few years
ipo_hist = yf.download('8TRA.ST STOR-B.ST EQT.ST SAVE.ST TRUE-B.ST OX2.ST ARION-SDB.ST HEM.ST MTRS.ST CARY.ST CINT.ST RVRC.ST' \
                       ' MCOV-B.ST ACAST.ST BHG.ST AMBEA.ST KAR.ST IMP-A-SDB.ST LINC.ST BOOZT.ST KFAST-B.ST THUNDR.ST' \
                       ' CTEK.ST NPAPER.ST CIBUS.ST NILAR.ST JOMA.ST WBGR-B.ST CS.ST',start='2017-01-01', end = '2021-10-20')
#byggfakta
#flatcapital

recent_ipo_closes = ipo_hist["Close"].dropna(how='all')#.fillna(0)
recent_ipo_open = ipo_hist["Open"].dropna(how='all')#.fillna(0)
recent_ipo_lows = ipo_hist["Low"].dropna(how='all')#.fillna(0)


op_cl_return = recent_ipo_closes/recent_ipo_open-1
op_low_return = recent_ipo_lows/recent_ipo_open-1


op_cl_return_bfill = op_cl_return.bfill(axis=0)
op_cl_return_first_trading_day = op_cl_return_bfill.iloc[0]

op_low_return_bfill = op_low_return.bfill(axis=0)
op_low_return_first_trading_day = op_low_return_bfill.iloc[0]

pd.concat([op_cl_return_first_trading_day,op_low_return_first_trading_day],axis=1)


#calculate summary statistics
avg = op_cl_return_first_trading_day.mean()
median = op_cl_return_first_trading_day.median()
vol = op_cl_return_first_trading_day.std()

kelly_f = avg/vol**2
kelly_f_trimmed_extreme_values = stats.trim_mean(op_cl_return_first_trading_day,0.05) / stats.mstats.trimmed_std(op_cl_return_first_trading_day,0.05)**2

