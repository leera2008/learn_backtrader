# Lesson2：Backtrader来啦：数据篇
# link: https://mp.weixin.qq.com/s/NTct2_AYhz4Z8q5MYtBQcA
#%%


#%%
import backtrader as bt
import pandas as pd
import datetime

import tushare as ts
import json
with open(r'Data/tushare_token.json','r') as load_json:
    token_json = json.load(load_json)
token = token_json['token']
ts.set_token(token) 
pro = ts.pro_api(token)
#%%

# 使用Tushare获取数据，要严格保持OHLC的格式

def get_data_bytushare(code,start_date,end_date):
    df = ts.pro_bar(ts_code=code, adj='qfq',start_date=start_date, end_date=end_date)
    #print(type(df))
    #df的数据类型是<class 'pandas.core.frame.DataFrame'>
    #pandas.core.frame.DataFrame 的方法如下：https://www.geeksforgeeks.org/python-pandas-dataframe/#:~:text=Pandas%20DataFrame%20is%20two-dimensional%20size-mutable%2C%20potentially%20heterogeneous%20tabular,three%20principal%20components%2C%20the%20data%2C%20rows%2C%20and%20columns.

    df = df[['trade_date', 'open', 'high', 'low', 'close','vol']]
    df.columns = ['trade_date', 'open', 'high', 'low', 'close','volume']

    #设置日期索引
    df.trade_date = pd.to_datetime(df.trade_date)
    #print("df.trade_date = ",type(df.trade_date),df.trade_date)
    #df.trade_date 的类型是pandas.core.series.Series
    #print(type(df.index))
    #在赋值之前df.index的类型是pandas.core.indexes.range.RangeIndex
    df.index = df.trade_date
    #print(type(df.index))
    #在赋值之后df.index的类型是pandas.core.indexes.datetimes.DatetimeIndex
    #排序
    df.sort_index(inplace=True) #用索引重新排序，其中in-place的意思是 “操作是直接改变给定线性代数、向量、矩阵(张量)的内容而不需要复制的运算”用来节约内存

    df.fillna(0.0,inplace=True) #空的项目用0替代

    return df

# 恒瑞医药
data1 = get_data_bytushare('600276.SH','20200101','20211015')
# 贵州茅台
data2 = get_data_bytushare('600519.SH','20200101','20211015')
# 海天味业
data3 = get_data_bytushare('603288.SH','20200101','20211015')
# 国泰君安
data4 = get_data_bytushare('601211.SH','20200101','20211015')

# %%

# 实例化策略
cerebro = bt.Cerebro()

st_date = datetime.datetime(2020,1,1)
ed_date = datetime.datetime(2021,10,15)

# 添加 600276.SH 的行情数据
datafeed1 = bt.feeds.PandasData(dataname=data1, fromdate=st_date, todate=ed_date)
cerebro.adddata(datafeed1, name='600276.SH')

# 添加 600519.SH 的行情数据
datafeed2 = bt.feeds.PandasData(dataname=data2, fromdate=st_date, todate=ed_date)
cerebro.adddata(datafeed2, name='600519.SH')

# 添加 603288.SH 的行情数据
datafeed3 = bt.feeds.PandasData(dataname=data3, fromdate=st_date, todate=ed_date)
cerebro.adddata(datafeed3, name='603288.SH')

#添加 601211.SH 的行情数据
datafeed4 = bt.feeds.PandasData(dataname=data4, fromdate=st_date, todate=ed_date)
cerebro.adddata(datafeed4, name='601211.SH')



#%%
# 第一章 DataFeed的数据结构

# 第1.1节：验证 data 的结构
class TestStrategy(bt.Strategy):
    def __init__(self):
        # 打印数据集和数据集对应的名称
#        print("-------------self.datas-------------")
#        print(self.datas) #是List类型，每个元素都是，backtrader.feeds.pandafeed.PandasData
#        print("-------------self.data-------------")
#        print(self.data._name, self.data) # 返回第一个导入的数据表格，缩写形式，类型和data0 以及data[0]一样都是PandasData
#        print("-------------self.data0-------------")
#        print(self.data0._name, self.data0) # 返回第一个导入的数据表格，缩写形式
        print("-------------self.datas[0]-------------")
        print(self.datas[0]._name, self.datas[0]) # 返回第一个导入的数据表格，常规形式
        print("-------------self.datas[1]-------------")
        print(self.datas[1]._name, self.datas[1]) # 返回第二个导入的数据表格，常规形式
        print("-------------self.datas[2]-------------")
        print(self.datas[2]._name, self.datas[2]) # 返回第三个导入的数据表格
        print("-------------self.datas[3]-------------")
        print(self.datas[3]._name, self.datas[3]) # 返回第四个导入的数据表格

        print("-------------换一种调用方式也是一样的-------------")
        print("-------------self.data0-------------")
        print(self.data0._name, self.data0) # 返回第一个导入的数据表格，常规形式
        print("-------------self.data1-------------")
        print(self.data1._name, self.data1) # 返回第二个导入的数据表格，常规形式
        print("-------------self.data2-------------")
        print(self.data2._name, self.data2) # 返回第三个导入的数据表格
        print("-------------self.data3-------------")
        print(self.data3._name, self.data3) # 返回第四个导入的数据表格


        print("--------- 打印 self 策略本身的 lines ----------")
        print(self.lines.getlinealiases())
        print("--------- 打印 self.datas 第一个数据表格的 lines ----------")
        print(self.datas[0].lines.getlinealiases())
        # 计算第一个数据集的s收盘价的20日均线，返回一个 Data feed #月线
        # 类 SimpleMovingAverage 是一个动态类，代码写在mabase.py里面，其实都是类MovingAverage
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0].close, period=20)
        print("--------- 打印 indicators 对象的 lines ----------")
        print(self.sma.lines.getlinealiases())
        print("---------- 直接打印 indicators 对象的所有 lines -------------")
        print(self.sma.lines)
        print("---------- 直接打印 indicators 对象的第一条 lines -------------")
        print(self.sma.lines[0])

    def next(self):
        print('验证索引位置为 6 的线是不是 datetime')
        # datetime 线中的时间点存的是数字形式的时间，可以通过 bt.num2date() 方法将其转为“xxxx-xx-xx xx:xx:xx”这种形式
        #print(bt.num2date(self.datas[0].lines[6][0]))
        print(self.datas[0].lines[0][0])
        print(self.datas[0].lines[1][0])
        print(self.datas[0].lines[2][0])
        print(self.datas[0].lines[3][0])
        print(self.datas[0].lines[4][0])
        print(self.datas[0].lines[5][0])
        print(self.datas[0].lines[6][0])

cerebro.addstrategy(TestStrategy)
result = cerebro.run()
