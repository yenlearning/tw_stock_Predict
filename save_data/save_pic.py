from datetime import date
import yfinance as yf
import pandas as pd
import time
import MySQLdb

t10_id=[2330, 2454, 2317, 2303, 2308, 2881, 1303, 1301, 2882, 2412]
t10_id = sorted(t10_id)
print(t10_id)

mysqldb= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='stock')
cursor = mysqldb.cursor()

from stocker import Stocker
# 存歷史圖 跟預言圖
for i in t10_id:
    stockNo = str(i) + ".TW"
    df = pd.read_csv('../static/stock_history/'+stockNo+'.csv')   
    df['Date']= pd.to_datetime(df['Date']) 
    df = df.sort_values(by='Date')
    df = df.reset_index(drop=True)

    stock = Stocker(stockNo, df)
    # stock.plot_stock(stockNo=str(i))#存歷史圖
    stock.changepoint_prior_scale = 0.14
    model, model_data =stock.create_prophet_model(stockNo=str(i), days=10)#存預測圖
    last_date=model_data[-10:]['yhat']
    date_upper=model_data[-10:]['yhat_upper']#上區間
    date_lower=model_data[-10:]['yhat_lower']#下區間
    def myRound(x):
        a=str(x).split('.',1)
        if int(a[1][2]) >= 5:
            x= x+0.01
            b= str(x).split('.',1)
            b[1]=b[1][:2]
            c = '.'
            b=c.join(b)
        else:
            b= str(x).split('.',1)
            b[1]=b[1][:2]
            c = '.'
            b=c.join(b)
        return float(b)
    day=1
    for j in last_date:
        # 存到資料庫
        cursor.execute("UPDATE `future` SET `day_%s_predict`= %s WHERE `stock_id`=%s",[(day),(myRound(j)),(i)])
        mysqldb.commit() #提交 此行一定要寫
        day=day+1

    day=1
    for k in date_upper:
        cursor.execute("UPDATE `future` SET `day_%s_upper`= %s WHERE `stock_id`=%s",[(day),(myRound(k)),(i)])
        mysqldb.commit() #提交 此行一定要寫
        day=day+1

    day=1
    for l in date_lower:
        cursor.execute("UPDATE `future` SET `day_%s_lower`= %s WHERE `stock_id`=%s",[(day),(myRound(l)),(i)])
        mysqldb.commit() #提交 此行一定要寫
        day=day+1
   


#------------------------------------------------------------------------------------------------

# # 存布林軌道圖
# for i in t10_id:
#     # 导入及处理数据
#     import pandas as pd
#     import numpy as np
#     # 绘图
#     import matplotlib.pyplot as plt
#     plt.cla()
#     print(plt.__file__)
#     # 设置图像标签显示中文
#     plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
#     plt.rcParams['axes.unicode_minus'] = False
#     import matplotlib as mpl

#     # 导入数据并做处理
#     def import_csv(stock_code):
#         df = pd.read_csv('../static/stock_history/'+stock_code + '.TW.csv')
#         df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')
#         df.set_index(['Date'], inplace=True)
#         return df
#     stock_code = str(i)
#     # 绘制数据的规模
#     scale = 500
#     df = import_csv(stock_code)[-scale:]
#     # SMA:简单移动平均(Simple Moving Average)
#     time_period = 20  # SMA的计算周期，默认为20
#     stdev_factor = 2  # 上下频带的标准偏差比例因子
#     history = []  # 每个计算周期所需的价格数据
#     sma_values = []  # 初始化SMA值
#     upper_band = []  # 初始化阻力线价格
#     lower_band = []  # 初始化支撑线价格
#     # 构造列表形式的绘图数据
#     for close_price in df['Close']:
#         #
#         history.append(close_price)

#         # 计算移动平均时先确保时间周期不大于20
#         if len(history) > time_period:
#             del (history[0])

#         # 将计算的SMA值存入列表
#         sma = np.mean(history)
#         sma_values.append(sma)  
#         # 计算标准差
#         stdev = np.sqrt(np.sum((history - sma) ** 2) / len(history))  
#         upper_band.append(sma + stdev_factor * stdev)
#         lower_band.append(sma - stdev_factor * stdev)

#     df = df.assign(a=pd.Series(df['Close'], index=df.index))
#     df = df.assign(b=pd.Series(sma_values, index=df.index))
#     df = df.assign(c=pd.Series(upper_band, index=df.index))
#     df = df.assign(d=pd.Series(lower_band, index=df.index))
#     # 绘图
#     ax = plt.figure(facecolor='white',figsize=(15,10))
#     # 设定y轴标签
#     ax.ylabel = df['Close']
#     plt.rc('legend', fontsize=16)
#     df['a'].plot(color='k', lw=1., legend=True,label='收盤價')
#     df['b'].plot(color='b', lw=1., legend=True,label='中界線')
#     df['c'].plot(color='r', lw=1., legend=True,label='阻力線')
#     df['d'].plot(color='g', lw=1., legend=True,label='支撐線')

#     plt.savefig("../static/img/img_bollin/bollin_"+str(i))
#     plt.close()




# #------------------------------------------------------------------------------------------------



# #  存技術分析圖K圖
# for i in t10_id:
#     import pandas as pd
#     import pandas_datareader as pdr
#     import matplotlib.pyplot as plt
#     plt.cla()
#     # 匯入資料，把csv檔(連結下方)放到與程式檔同一資料夾
#     df = pd.read_csv('../static/stock_history/'+str(i)+'.TW.csv',parse_dates=['Date'],index_col=0).dropna()
#     df = df[(df.index > '2021-02-01')]
#     df_plot = df[['Open','High','Low','Close']]

#     #計算MA線
#     def moving_average(data,period):
#         return data['Close'].rolling(period).mean()

#     data_df = df.copy()
#     data_df['min'] = data_df['Low'].rolling(9).min()
#     data_df['max'] = data_df['High'].rolling(9).max()
#     data_df['RSV'] = (data_df['Close'] - data_df['min'])/(data_df['max'] - data_df['min'])
#     data_df = data_df.dropna()
#     #把有空值的筆(前8筆) 丟掉
#     # 計算K
#     # K的初始值定為50
#     K_list = [50]
#     data_df.head(10)

#     #計算KD線
#     '''
#     Step1:計算RSV:(今日收盤價-最近9天的最低價)/(最近9天的最高價-最近9天的最低價)
#     Step2:計算K: K = 2/3 X (昨日K值) + 1/3 X (今日RSV)
#     Step3:計算D: D = 2/3 X (昨日D值) + 1/3 X (今日K值)
#     '''
#     def KD(data):
#         data_df = data.copy()
#         data_df['min'] = data_df['Low'].rolling(9).min()
#         data_df['max'] = data_df['High'].rolling(9).max()
#         data_df['RSV'] = (data_df['Close'] - data_df['min'])/(data_df['max'] - data_df['min'])
#         data_df = data_df.dropna()
#         # 計算K
#         # K的初始值定為50
#         K_list = [50]
#         for num,rsv in enumerate(list(data_df['RSV'])):
#             K_yestarday = K_list[num]
#             K_today = 2/3 * K_yestarday + 1/3 * rsv
#             K_list.append(K_today)
#         data_df['K'] = K_list[1:]
#         # 計算D
#         # D的初始值定為50
#         D_list = [50]
#         for num,K in enumerate(list(data_df['K'])):
#             D_yestarday = D_list[num]
#             D_today = 2/3 * D_yestarday + 1/3 * K
#             D_list.append(D_today)
#         data_df['D'] = D_list[1:]
#         use_df = pd.merge(data,data_df[['K','D']],left_index=True,right_index=True,how='left')
#         return use_df
            
#     df = KD(df)
#     df.tail()

#     from matplotlib import dates as mdates
#     from matplotlib import ticker as mticker
#     from mplfinance.original_flavor import candlestick_ohlc
#     import mplfinance
#     from matplotlib.dates import DateFormatter
#     import datetime as dt

#     def prepare_data(data):
#         data_df = data.copy()
#         data_df['DateTime'] = data_df.index
#         data_df = data_df.reset_index()
#         data_df = data_df[['DateTime','Open','High','Low','Close']]
#         data_df['DateTime'] = mdates.date2num(data_df['DateTime'].astype('datetime64[ns]'))
#         return data_df

#     # 畫股價圖
#     # 顏色:https://matplotlib.org/users/colors.html
#     #畫股價線圖與蠟燭圖
#     def plot_stock_price(data):
#         Ma_10 = moving_average(data,10)
#         Ma_50 = moving_average(data,50)
#         Length = len(data['DateTime'].values[50-1:])
#         plt.figure(facecolor='white',figsize=(15,10))
#         ax1 = plt.subplot2grid((6,4), (0,0),rowspan=4, colspan=4, facecolor='w')
#         candlestick_ohlc(ax1, data.values[-Length:],width=0.6,colorup='red',colordown='green')
#         Label1 = '10 MA Line'
#         Label2 = '50 MA Line'
#         ax1.plot(data.DateTime.values[-Length:],Ma_10[-Length:],'black',label=Label1, linewidth=1.5)
#         ax1.plot(data.DateTime.values[-Length:],Ma_50[-Length:],'navy',label=Label2, linewidth=1.5)
        
#         box=ax1.get_position()
#         ax1.set_position([box.x0, box.y0, box.width , box.height* 0.8])
#         ax1.legend(loc='center',bbox_to_anchor=(0.5, 1.1),ncol=3)
        

#         ax1.grid(True, color='black')
#         ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#         ax1.yaxis.label.set_color("black")
#         plt.ylabel('Stock price and Volume')
#         plt.suptitle('Stock Code:'+str(i),color='black',fontsize=16)
#         #畫交易量
#         ax1v = ax1.twinx()
#         ax1v.fill_between(data.DateTime.values[-Length:],0, df.Volume.values[-Length:], facecolor='navy', alpha=.4)
#         ax1v.axes.yaxis.set_ticklabels([])
#         ax1v.grid(False)
#         ax1v.set_ylim(0, 3*df.Volume.values.max())
#         #加入KD線在下方
#         ax2 = plt.subplot2grid((6,4), (5,0), sharex=ax1, rowspan=1, colspan=4, facecolor='white')
#         ax2.plot(daysreshape.DateTime.values[-Length:], df.K[-Length:],color='black')
#         ax2.plot(daysreshape.DateTime.values[-Length:], df.D[-Length:],color='navy')
#         plt.ylabel('KD Value', color='black')
        
#     daysreshape = prepare_data(df_plot)
#     plot_stock_price(daysreshape)

#     plt.savefig("../static/img/img_K/K_"+str(i)+".png")   



# #------------------------------------------------------------------------------------------------

# for i in t10_id:
#     # 存成交量圖
#     import mpl_finance as mpf
#     import matplotlib.pyplot as plt
#     import pandas as pd
#     import matplotlib.ticker as ticker
#     import numpy as np
#     #创建绘图的基本参数
#     fig, axes = plt.subplots(2, 1, sharex=True, figsize=(15, 10))
#     ax1, ax2 = axes.flatten()

#     #获取刚才的股票数据
#     stock_id=i
#     df = pd.read_csv(f'../static/stock_history/{stock_id}.TW.csv', parse_dates=True)
#     mpf.candlestick2_ochl(ax1, df["Open"], df["Close"], df["High"], df["Low"], width=0.6, colorup='r',colordown='green',alpha=1.0)
#     df['Date'] = pd.to_datetime(df['Date'])
#     df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
#     def format_date(x, pos=None):
#         if x < 0 or x > len(df['Date']) - 1:
#             return ''
#         return df['Date'][int(x)]
#     df["SMA5"] = df["Close"].rolling(5).mean()
#     df["SMA10"] = df["Close"].rolling(10).mean()
#     df["SMA30"] = df["Close"].rolling(30).mean()
#     ax1.plot(np.arange(0, len(df)), df['SMA5'],label="SMA5")  # 绘制5日均线
#     ax1.plot(np.arange(0, len(df)), df['SMA10'],label="SMA10")  # 绘制10日均线
#     ax1.plot(np.arange(0, len(df)), df['SMA30'],label="SMA30")  # 绘制30日均线
#     ax1.legend(loc='upper center', ncol=3,fontsize=20)


#     ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
#     plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

#     red_pred = np.where(df["Close"] > df["Open"], df["Volume"], 0)
#     blue_pred = np.where(df["Close"] < df["Open"], df["Volume"], 0)
#     ax2.bar(np.arange(0, len(df)), red_pred, facecolor="red")
#     ax2.bar(np.arange(0, len(df)), blue_pred, facecolor="blue")
#     fig.tight_layout()
#     #显示出来
#     plt.savefig("../static/img/img_volume/volume_"+str(i))
    