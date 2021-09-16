import pandas as pd
import numpy as np

class EMA_class:
    def __init__(self,df, base, target, period, alpha=False):
        self.df=df
        self.base=base
        self.target=target
        self.period=period
        self.alpha=alpha

    def EMA(self):
        con = pd.concat([self.df[:self.period][self.base].rolling(window=self.period).mean(), self.df[self.period:][self.base]])

        if (self.alpha == True):
            # (1 - alpha) * previous_val + alpha * current_val where alpha = 1 / period
            self.df[self.target] = con.ewm(alpha=1 / self.period, adjust=False).mean()
        else:
            # ((current_val - previous_val) * coeff) + previous_val where coeff = 2 / (period + 1)
            self.df[self.target] = con.ewm(span=self.period, adjust=False).mean()

        self.df[self.target].fillna(0, inplace=True)
        return self.df

class SuperTrend:
    def __init__(self,df, period, multiplier, ohlc=['Open', 'High', 'Low', 'Close']):
        self.df=df
        self.period=period
        self.multiplier=multiplier
        self.ohlc=ohlc


    def supertrend_calc(self):

        self.ATR()
        atr = 'ATR_' + str(self.period)
        st = 'ST_' + str(self.period) + '_' + str(self.multiplier)
        stx = 'STX_' + str(self.period) + '_' + str(self.multiplier)



        # Compute basic upper and lower bands
        self.df['basic_ub'] = (self.df[self.ohlc[1]] + self.df[self.ohlc[2]]) / 2 + self.multiplier * self.df[atr]
        self.df['basic_lb'] = (self.df[self.ohlc[1]] + self.df[self.ohlc[2]]) / 2 - self.multiplier * self.df[atr]

        # Compute final upper and lower bands
        self.df['final_ub'] = 0.00
        self.df['final_lb'] = 0.00
        for i in range(self.period, len(self.df)):
            self.df['final_ub'].iat[i] = self.df['basic_ub'].iat[i] if self.df['basic_ub'].iat[i] < self.df['final_ub'].iat[i - 1] or \
                                                             self.df[self.ohlc[3]].iat[i - 1] > self.df['final_ub'].iat[i - 1] else \
                self.df['final_ub'].iat[i - 1]
            self.df['final_lb'].iat[i] = self.df['basic_lb'].iat[i] if self.df['basic_lb'].iat[i] > self.df['final_lb'].iat[i - 1] or \
                                                             self.df[self.ohlc[3]].iat[i - 1] < self.df['final_lb'].iat[i - 1] else \
                self.df['final_lb'].iat[i - 1]

        # Set the Supertrend value
        self.df[st] = 0.00
        for i in range(self.period, len(self.df)):
            self.df[st].iat[i] = self.df['final_ub'].iat[i] if self.df[st].iat[i - 1] == self.df['final_ub'].iat[i - 1] and self.df[self.ohlc[3]].iat[
                i] <= self.df['final_ub'].iat[i] else \
                self.df['final_lb'].iat[i] if self.df[st].iat[i - 1] == self.df['final_ub'].iat[i - 1] and self.df[self.ohlc[3]].iat[i] > \
                                         self.df['final_ub'].iat[i] else \
                    self.df['final_lb'].iat[i] if self.df[st].iat[i - 1] == self.df['final_lb'].iat[i - 1] and self.df[self.ohlc[3]].iat[i] >= \
                                             self.df['final_lb'].iat[i] else \
                        self.df['final_ub'].iat[i] if self.df[st].iat[i - 1] == self.df['final_lb'].iat[i - 1] and self.df[self.ohlc[3]].iat[i] < \
                                                 self.df['final_lb'].iat[i] else 0.00

        # Mark the trend direction up/down
        self.df[stx] = np.where((self.df[st] > 0.00), np.where((self.df[self.ohlc[3]] < self.df[st]), 'down', 'up'), np.NaN)

        # Remove basic and final bands from the columns
        self.df.drop(['basic_ub', 'basic_lb', 'final_ub', 'final_lb',f'{st}',f'{atr}','TR'], inplace=True, axis=1)

        self.df.fillna(0, inplace=True)

        return self.df

    def ATR(self,ohlc=['Open', 'High', 'Low', 'Close']):
        atr = 'ATR_' + str(self.period)

        # Compute true range only if it is not computed and stored earlier in the df
        if not 'TR' in self.df.columns:
            self.df['h-l'] = self.df[ohlc[1]] - self.df[ohlc[2]]
            self.df['h-yc'] = abs(self.df[ohlc[1]] - self.df[ohlc[3]].shift())
            self.df['l-yc'] = abs(self.df[ohlc[2]] - self.df[ohlc[3]].shift())

            self.df['TR'] = self.df[['h-l', 'h-yc', 'l-yc']].max(axis=1)

            self.df.drop(['h-l', 'h-yc', 'l-yc'], inplace=True, axis=1)

        # Compute EMA of true range using ATR formula after ignoring first row
        EMA_class(self.df, 'TR', atr, self.period, alpha=True).EMA()

        return self.df

