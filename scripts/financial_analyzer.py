import pandas as pd
import talib
import pynance as py
from pynance import Analyzer

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
    
    #The following functions are used to calculate financial metrics using pynance

    def calculate_sharpe_ratio(self, risk_free_rate=0.0):
        """
        Calculates the Sharpe Ratio for each stock.

        Parameters:
        ----------
        risk_free_rate : float, optional
            The risk-free rate to be used in the Sharpe Ratio calculation, by default 0.0.

        Returns:
        -------
        dict
            A dictionary where the keys are stock tickers and values are the Sharpe Ratios.
        """
        sharpe_ratios = {}
        for ticker, df in self.data.items():
            returns = df['Close'].pct_change().dropna()          
            excess_returns = returns - risk_free_rate
            sharpe_ratio = excess_returns.mean() / excess_returns.std()
            sharpe_ratios[ticker] = sharpe_ratio
        return sharpe_ratios()

    def calculate_pynance_metrics(self, price_col='Close'):
        """
        Calculates financial metrics using pynance.Analyzer.
        This method demonstrates how to integrate pynance into your analysis.
        Args:
            price_col (str): The name of the column containing the price data
                             that pynance should use (e.g., 'Close').
        Returns:
            pd.DataFrame: DataFrame with pynance-derived metrics added.
        """
        if price_col not in self.df.columns:
            print(f"Error: '{price_col}' column not found in DataFrame for PyNance analysis.")
            return self.df

        pynance_data = self.df[[price_col]].copy()
        if price_col != 'Close':
            pynance_data.rename(columns={price_col: 'Close'}, inplace=True)

        try:
            # Initialize the PyNance Analyzer
            analyzer = Analyzer(pynance_data)

            # Example: Calculate cumulative returns
            # PyNance's returns property provides various return calculations
            cumulative_returns = analyzer.returns.cumulative()
            self.df['Cumulative_Return_PyNance'] = cumulative_returns

            # Example: Calculate daily log returns (another common metric)
            # log_returns = analyzer.returns.log_daily()
            # self.df['Log_Daily_Return_PyNance'] = log_returns

            print("Calculated PyNance metrics (e.g., Cumulative Return).")
        except Exception as e:
            print(f"An error occurred while using PyNance: {e}")
        return self.df
