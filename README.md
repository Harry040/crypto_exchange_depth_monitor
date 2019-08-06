## 主要用途
此脚本抓取各个交易所深度数据，供交易作为参考

## 数据说明
```
time@2019-08-06 17:11:12.175686
exchange  bid_s001  ask_s001
   huobi      2.66      0.00
 binance      2.77      2.47
bitfinex      3.38      4.90
coinbase      1.67      3.26
bitstamp      2.36      3.98
--------
exchange  bid_s005  ask_s005
   huobi      0.00      0.00
 binance      0.00      0.00
bitfinex      9.38     19.17
coinbase      4.07     12.42
bitstamp      6.13     11.32
--------
exchange  bid_s010  ask_s010
   huobi      0.00      0.00
 binance      0.00      0.00
bitfinex     20.20     36.34
coinbase     14.52     23.77
bitstamp     11.36     13.94
```
分三个级别作为监控:
第一级别
1. bid_s001是价格一价格区间买盘的统计量,单位是1M美元. 此区间为:假设当前买一价为bid1，此区间为[bid1*0.99,bid1]
2. ask_s001是价格一价格区间卖盘的统计量,单位是1M美元. 此区间为:假设当前卖一价为ask1，此区间为[ask1, ask1*1.01]

第二级别
1. bid_s005是价格一价格区间买盘的统计量,单位是1M美元. 此区间为:假设当前买一价为bid1，此区间为[bid1*0.95,bid1]
1. ask_s005是价格一价格区间卖盘的统计量,单位是1M美元. 此区间为:假设当前卖一价为ask1，此区间为[ask1, ask1*1.05]

第三级别
1. bid_s010是价格一价格区间买盘的统计量,单位是1M美元. 此区间为:假设当前买一价为bid1，此区间为[bid1*0.90,bid1]
1. ask_s010是价格一价格区间卖盘的统计量,单位是1M美元. 此区间为:假设当前卖一价为ask1，此区间为[ask1, ask1*1.10]


## 代码模块
1. orderbook.py 负责从各交易所提取深度数据,放入sqlite中,可以设置个定时任务一定周期去抓取数据
2. utils_db.py, 负责数据的插入和读取

```
python orderbook.py
python utils_db.py
```

可以入群[telegram](https://t.me/monitor_marketssss)输入 ```/depth```即可查看深度数据
