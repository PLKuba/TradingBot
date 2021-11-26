VERSION="v1"
print(VERSION)

import ccxt,pandas as pd
from indicators import EMA_class,SuperTrend
from datetime import datetime
from binance.client import Client
import schedule,time


from sms import send_mail
import futures_test as futures

from config import API_KEY,API_SECRET
exchange=ccxt.binance()
client=Client(API_KEY,API_SECRET)

settings={
    "symbol":"BTCUSDT",
    "cost":0,
    "timeframe":"15m",
    "ema_period":200,
    "in_long_position" : False,
    "in_short_position" : False,
    "closed_long":False,
    "closed_short" : False
}

def check_buy_sell_signals(df, symbol,settings,trade_time):
    in_long_position=settings["in_long_position"]
    in_short_position=settings["in_short_position"]
    closed_long=settings["closed_long"]
    closed_short=settings["closed_short"]


    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1
    print(settings["in_short_position"],settings["in_long_position"],settings["closed_short"],settings["closed_long"])

    symbol = settings["symbol"]
    price = df["Close"][last_row_index]

    if not closed_short and in_short_position and df["STX_12_3"][last_row_index] == "up":
        futures.cancel_sell_order(symbol)
        send_mail("Close short", f"Closed {symbol} at ${price}")

        df["SHORT ACTION"][last_row_index] = "CLOSE SHORT"
        print("CLOSE SHORT")

        closed_short = True
        in_short_position = False
        in_long_position = False

    if not closed_long and in_long_position and df["STX_12_3"][last_row_index] == "down":
        futures.cancel_buy_order(symbol)
        send_mail("Close long", f"Shorted {symbol} at ${price}")

        df["LONG ACTION"][last_row_index] = "CLOSE LONG"
        print("CLOSE LONG")

        closed_long = True
        in_long_position = False
        in_long_position = False



    if df["EMA"][last_row_index]>df["Close"][last_row_index]:
    #    price is below EMA
        if not in_short_position:
            if df["STX_12_3"][last_row_index]=="down":
                futures.sell(symbol, settings["cost"])

                send_mail("Open short", f"Shorted {symbol} at ${price}")

                df["SHORT ACTION"][last_row_index] = "OPEN SHORT"
                print("OPEN SHORT")


                in_short_position = True
                in_long_position = False
                closed_short = False

    else:
    #    price is above EMA
        if not in_long_position:
            if df["STX_12_3"][last_row_index]=="up":
                futures.buy(symbol, settings["cost"])

                send_mail("Open long", f"Longed {symbol} at ${price}")

                df["LONG ACTION"][last_row_index] = "OPEN LONG"
                print("OPEN LONG")


                in_long_position=True
                in_short_position=False
                closed_long = False

    settings["in_long_position"]=in_long_position
    settings["in_short_position"]=in_short_position
    settings["closed_long"]=closed_long
    settings["closed_short"]=closed_short

def run_bot(settings):
    balance = client.futures_account_balance(timestamp=datetime.now().timestamp())
    for item in balance:
        if item["asset"] == "USDT":
            usdt_balance = int(float(item["balance"]))
            settings["cost"]=int(float(usdt_balance/10))
            temp_cost=settings["cost"]
            print(f"cost: {temp_cost}")
            break

    print("waiting for the candle to close")
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if int(current_time[6]) == 0 and int(current_time[7])==1:
            break

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    binance_currencies = settings["symbol"]
    ccxt_currencies = binance_currencies.replace("USDT", "/USDT")

    print(f"Fetching new bars for {binance_currencies}")
    print("#########")
    print(current_time)
    print("#########\n")


    bars = exchange.fetch_ohlcv(symbol=ccxt_currencies, limit=1000, timeframe=settings["timeframe"])
    df = pd.DataFrame(bars[:-1], columns=["timestamp", "Open", "High", "Low", "Close", "volume"])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df["LONG ACTION"]='-'
    df["SHORT ACTION"]='-'

    supertrend_12_3 = SuperTrend(df, period=12, multiplier=3).supertrend_calc()
    ema = EMA_class(df, base="Close", target="EMA", period=settings["ema_period"]).EMA()

    check_buy_sell_signals(df, symbol=settings["symbol"],trade_time=current_time,settings=settings)
    print(df.tail(10))


def interval(timeframe):
    if len(timeframe)==3:
        num = timeframe[0] + timeframe[1]
        if timeframe[2]=='m':
            interval=60*int(num)-10
            return(interval)
        elif timeframe[2]=='h':
            interval=3600*int(num)-10
            return(interval)
    else:
        if timeframe[1]=='m':
            interval=60*int(timeframe[0])-10
            return(interval)
        elif timeframe[1]=='h':
            interval=3600*int(timeframe[0])-10
            return(interval)
        elif timeframe[1]=='d':
            interval = 3600*24*int(timeframe[0])-10
            return (interval)
        elif timeframe[1]=='w':
            interval = 3600*24*7*int(timeframe[0])-10
            return (interval)
        elif timeframe[1] == 'M':
            interval = 2628*1000*int(timeframe[0])-10
            return (interval)

position = client.futures_position_information(symbol=settings["symbol"])
position_size_float = float(position[0]["positionAmt"])

if position_size_float<0.00:
    settings["in_short_position"]=True
elif position_size_float>0.00:
    settings["in_long_position"]=True

schedule.every(1).seconds.do(run_bot,settings=settings)

while True:
    schedule.run_pending()
    time.sleep(1)
