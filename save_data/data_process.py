# 存CSV

#獲取台灣50的所有id
# 必須先安裝yfinance套件
# pip install yfinance
import yfinance as yf
import pandas as pd
import time

df=pd.read_csv('T50.csv')  
# print(df)
t50_id=[]
for i in range(50):
    t50_id.append(df["證券代碼"].loc[i])
t50_id = sorted(t50_id)
print(t50_id)

#-----------------------------------------
have_na=[]

for id in t50_id:    
    # 抓取股票資料
    stock_id = str(id) + '.TW'
    # data = yf.Ticker(stock_id)
    # df = data.history(period="max")

    data=yf.download(stock_id,start='2016-08-01')
    # print(data)
    # print("這裡是",id)
    # print(data.isnull().any())

    #用前後筆平均補空值
    data=data.interpolate()
    
    #涵有空值的行數 如果 >0
    if data.isnull().any(axis=1).sum()>0: 
        # print('{} 有 {} 筆資料有空值'.format(id,data.isnull().any(axis=1).sum()))    
        have_na.append([id,data.isnull().any(axis=1).sum()])
    print("------------------------------------------------------")

    # 合併
    # historical_data = pd.concat([historical_data, df])
    # time.sleep(0.8)

    data.to_csv('../static/stock_history/'+stock_id+'.csv', index=True, header = True)

#有空值的:2892 2886 
print("有空值的資料有:\n",have_na)