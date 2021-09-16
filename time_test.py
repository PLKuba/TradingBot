import futures_test as futures
from binance.client import Client
import time,math
client = Client("m0NJtJo4u1uIv07yu7lFrcWBnVUDhqHiykLvWMe3V2PArQlsE6ja89Xm8K5ebEes","aK8eOMK1ykDqy7vw8LqYE9X1jFrULlN25kqUZEKAV0c68qoi7WIQAhsx8mUTrKkf")
"""greyed out part is reading coins from txt file"""
with open("coins.txt", mode="r") as file:
    text=file.read()

currencies=[]
coin = ""

for item in text:
    if item=="." or item=="\n":
        if coin=='':
            continue
        currencies.append(coin)
        coin=""
        continue
    coin+=item

binance_currencies=currencies
ccxt_currencies=[]

for item in currencies:
    new_item=item.replace("USDT","/USDT")
    ccxt_currencies.append(new_item)

