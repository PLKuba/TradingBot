from binance.client import Client
import math

client = Client("m0NJtJo4u1uIv07yu7lFrcWBnVUDhqHiykLvWMe3V2PArQlsE6ja89Xm8K5ebEes","aK8eOMK1ykDqy7vw8LqYE9X1jFrULlN25kqUZEKAV0c68qoi7WIQAhsx8mUTrKkf")

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def calculate_precision(symbol):
    data=client.futures_order_book(symbol=symbol)
    order=data["bids"][0][1]
    precision=0
    for char in order:
        if char=='.' or precision>0:
            precision+=1
    if precision!=0:
        precision-=1
    return precision


def calculate_precicion(symbol,value,timeframe,leverage=10):
    client.futures_change_leverage(symbol=symbol, leverage=10)

    value=value*leverage

    kline = client.get_klines(symbol=symbol, interval=timeframe, limit=1)
    for item in kline:
        quantity=value/float(item[4])

    precision=calculate_precision(symbol)
    quantity=truncate(quantity,precision)

    return quantity

def calculate_precicion_backtest(symbol,value,timeframe,leverage=10,entryPrice=0):
    client.futures_change_leverage(symbol=symbol, leverage=leverage)

    value=value*leverage
    quantity=value/entryPrice


    precision=calculate_precision(symbol)

    quantity=truncate(quantity,precision)

    return quantity

def buy(symbol,cost):
    order = client.futures_create_order(symbol=symbol, side='BUY', type='MARKET', quantity=calculate_precicion(symbol=symbol,value=cost,timeframe="1m",leverage=10))
def cancel_buy_order(symbol):
    position = client.futures_position_information(symbol=symbol)
    position_size_float = float(position[0]["positionAmt"])
    if position_size_float!=0.00:
        position=client.futures_position_information(symbol=symbol)
        if float(position[0]["positionAmt"])<0:
            position_quantity=float(position[0]["positionAmt"])*-1
        else:
            position_quantity = float(position[0]["positionAmt"])
        client.futures_create_order(symbol=symbol, side='SELL', type='MARKET', quantity=position_quantity)
    else:
        print("nothing to cancel")

def cancel_sell_order(symbol):
    position = client.futures_position_information(symbol=symbol)
    position_size_float = float(position[0]["positionAmt"])
    if position_size_float != 0.00:
        position = client.futures_position_information(symbol=symbol)
        if float(position[0]["positionAmt"])<0:
            position_quantity=float(position[0]["positionAmt"])*-1
        else:
            position_quantity = float(position[0]["positionAmt"])
        client.futures_create_order(symbol=symbol, side='BUY', type='MARKET',quantity=position_quantity)
    else:
        print("nothing to cancel")

def sell(symbol,cost):
    order = client.futures_create_order(symbol=symbol, side='SELL', type='MARKET', quantity=calculate_precicion(symbol=symbol,value=cost,timeframe="1m",leverage=10))
