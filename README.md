# TradingBot

This is a crypto trading bot that supports Binance® exchange.

Backtesting results:
I will be visible in the backtesting.txt file -> UNDER THE MAINTENANCE

So far I managed to grow my account 89,6% in two months.

In order to make it works, fork youw own copy and do the following:

1) Head to Binance.com then -> Profile -> API Management and create API Key.
NOTE: save Secret Key right away as it will only appear once while creating it.

2) Fill obtained keys in the config.py file
The script also contains SMS notifications when action is taken.
3) Also in config.py insert your email and email application password. In order to create app password head to https://myaccount.google.com/apppasswords and create one. It should look something like this: XXXX-XXXX-XXXX-XXXX
You are good to go, and you will be notified every time an action will occur.

General info about a strategy:
This script is based on the Supertrend calculation and EMA200.
Basic rules:

If price close is above EMA and supertrend has turned to up, you go long.
If price close is below EMA and supertrend has turned to down, you go short.

You close either positions when then trend direction changes.

Default settings:
Symbol: BTCUSDT
Timeframe: 15m
EMA: 200
Supertrend: (period:12,multiplier:3)
Leverage:10
Position size: 10% of your portfolio

All things are changable

Happy trading and coding everyone!
