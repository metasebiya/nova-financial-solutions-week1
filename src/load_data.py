"""
load_data.py - Data loading functions for financial data analysis

This module contains functions to load financial data from various sources
for the nova-financial-solutions-week1 project.

Author: [Metasebiya Bizuneh]
Created: May 29, 2025
"""

import os
import pandas as pd

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
