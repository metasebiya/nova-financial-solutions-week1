import pandas as pd
import talib

class FinancialAnalyzer:
    def __init__(self, dataframe):
        self.df = dataframe.copy()

    def calculate_moving_averages(self, price_col='Close', periods=[10, 20, 50]):
        for period in periods:
            self.df[f'SMA_{period}'] = talib.SMA(self.df[price_col], timeperiod=period)
        print(f"Calculated SMAs for periods: {periods}")
        return self.df

    def calculate_rsi(self, price_col='Close', period=14):
        self.df['RSI'] = talib.RSI(self.df[price_col], timeperiod=period)
        print(f"Calculated RSI with period: {period}")
        return self.df

    def calculate_macd(self, price_col='Close', fastperiod=12, slowperiod=26, signalperiod=9):
        macd, macdsignal, macdhist = talib.MACD(
            self.df[price_col],
            fastperiod=fastperiod,
            slowperiod=slowperiod,
            signalperiod=signalperiod
        )
        self.df['MACD'] = macd
        self.df['MACD_Signal'] = macdsignal
        self.df['MACD_Hist'] = macdhist
        print("Calculated MACD.")
        return self.df

    def calculate_daily_returns(self, price_col='Close'):
        if price_col in self.df.columns:
            self.df = self.df.sort_index()
            self.df['Daily_Return'] = self.df[price_col].pct_change() * 100
            print("Calculated daily stock returns.")
        else:
            print(f"Error: '{price_col}' column not found to calculate daily returns.")
        return self.df