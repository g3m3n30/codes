# -*- coding: utf-8 -*-
"""binancep2p.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/g3m3n30/codes/blob/main/binancep2p.ipynb
"""

"""pip install matplotlib
    This does not work somehow.
"""
!pip install matplotlib

import numpy as np
import requests
import pandas as pd
"""import matplotlib.pyplot as plt
"""
from matplotlib import pyplot as plt
import seaborn as sns
from datetime import datetime
now = datetime.now()
current_time = now.strftime("%d-%b-%Y %H:%M:%S")

link = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
payload = {"proMerchantAds":False,"page":1,"rows":20,"payTypes":[],"countries":[],"publisherType":None,"asset":"USDT","fiat":"MMK","tradeType":"BUY"}

with requests.Session() as s:
    s.headers.update(headers)
    res = s.post(link,json=payload)


data = res.json()['data']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
payload = {"proMerchantAds":False,"page":1,"rows":20,"payTypes":[],"countries":[],"publisherType":None,"asset":"USDT","fiat":"MMK","tradeType":"SELL"}

with requests.Session() as s:
    s.headers.update(headers)
    res = s.post(link,json=payload)

data2 = res.json()['data']
data.extend(data2)

link = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
payload = {"proMerchantAds":False,"page":2,"rows":20,"payTypes":[],"countries":[],"publisherType":None,"asset":"USDT","fiat":"MMK","tradeType":"BUY"}

with requests.Session() as s:
    s.headers.update(headers)
    res = s.post(link,json=payload)

data2 = res.json()['data']
data.extend(data2)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
payload = {"proMerchantAds":False,"page":2,"rows":20,"payTypes":[],"countries":[],"publisherType":None,"asset":"USDT","fiat":"MMK","tradeType":"SELL"}

with requests.Session() as s:
    s.headers.update(headers)
    res = s.post(link,json=payload)

data2 = res.json()['data']
data.extend(data2)

result = [dict(pair for d1 in d.values() for pair in d1.items()) for d in data]
x = list(map(lambda x: x["price"], result))
y = list(map(lambda y: y["tradableQuantity"], result))
z = list(map(lambda z: z["tradeType"], result))
combineddata = [{'price':price, 'limit': limit, 'buysell': buysell} for price, limit, buysell in zip(x,y,z)]
df = pd.DataFrame(data=combineddata)

df.price = df.price.astype("float")
df.limit = df.limit.astype("float")
df.buysell = df.buysell.astype("str")
buy = df.loc[df.buysell=='BUY']
sell = df.loc[df.buysell=='SELL']
#round the numbers by 25
def round_25(number):
    return (25*round(number/25))
min_round = round_25((min(df.price)))
max_round = round_25((max(df.price)))

fig, ax = plt.subplots()

ax.set_title(f"Last update: {current_time}")
sns.ecdfplot(x="price", weights="limit",stat="count", data=sell, ax=ax)
sns.ecdfplot(x="price", weights="limit",stat="count",complementary=True, data=buy, ax=ax)

sns.scatterplot(x="price", y="limit", hue="buysell",  data=df, ax=ax)

ax.set_xlabel("Price")
ax.set_ylabel("depth($)")
ax.set_yscale('log')

ax.set_xticks(np.arange(min_round,max_round+1, 25)) #working one
ax.set_yticks([100, 250, 500, 1000, 2000, 5000, 10000, 50000, 100000, 200000, 500000, 1000000],[100, 250, 500, "1k", "2k", "5k", "10k", "50k", "100k", "200k", "500k", "1M"])

plt.show()

