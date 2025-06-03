"""
load_data.py - Data loading functions for financial data analysis

This module contains functions to load financial data from various sources
for the nova-financial-solutions-week1 project.

Author: [Metasebiya Bizuneh]
Created: May 29, 2025
"""

import os
import pandas as pd


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(file_path):
        """
        Load a CSV file into a pandas DataFrame for financial analysis

        Parameters:
            file_path (str): Path to the CSV file (e.g., 'data/raw/financial_data.csv')

        Returns:
            pd.DataFrame: Loaded financial data as a DataFrame

        Raises:
            FileNotFoundError: If the specified file does not exist
        """

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")
        df = pd.read_csv(file_path)
        return df

    def load_local_stock_data(self, stock_files_info):
        """
        Loads historical stock price data from local CSV files for multiple tickers.
        Args:
            stock_files_info (dict): A dictionary where keys are ticker symbols
                                     and values are the file paths to their respective CSVs.
                                     Example: {'AAPL': '../data/AAPL.csv', 'GOOG': '../data/GOOG.csv'}
        Returns:
            dict: A dictionary where keys are ticker symbols and values are
                  pd.DataFrames containing the loaded stock data.
        """
        all_stock_dfs = {}
        for ticker, file_path in stock_files_info.items():
            try:
                print(f"Loading stock data for {ticker} from {file_path}...")
                df = pd.read_csv(file_path)
                df['Ticker'] = ticker # Add a ticker column to identify the stock
                
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                    df.dropna(subset=['Date'], inplace=True)
                    df.set_index('Date', inplace=True) 
                    df.sort_index(inplace=True) 
                elif 'date' in df.columns: 
                     df['date'] = pd.to_datetime(df['date'], errors='coerce')
                     df.dropna(subset=['date'], inplace=True)
                     df.rename(columns={'date': 'Date'}, inplace=True)
                     df.set_index('Date', inplace=True)
                     df.sort_index(inplace=True)
                else:
                    print(f"Warning: No 'Date' or 'date' column found in {file_path}. Skipping.")
                    continue

                # Ensure numerical columns are numeric
                numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                for col in numeric_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                # Drop rows where critical price/volume data might be missing after conversion
                df.dropna(subset=['Close', 'Volume'], inplace=True) 

                all_stock_dfs[ticker] = df
                print(f"Successfully loaded stock data for {ticker}.")
            except FileNotFoundError:
                print(f"Error: Stock file not found at {file_path} for ticker {ticker}.")
            except Exception as e:
                print(f"An error occurred while loading stock data for {ticker} from {file_path}: {e}")
        return all_stock_dfs
