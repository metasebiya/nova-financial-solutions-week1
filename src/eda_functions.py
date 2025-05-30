"""
eda_functions.py - EDAda Processing functions for financial data analysis

This module contains functions to perform several EDA prcocess on financial data from various sources
for the nova-financial-solutions-week1 project.

Author: [Metasebiya Bizuneh]
Created: May 29, 2025
"""
from typing import Dict
import pandas as pd
import load_data as ld
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


def descriptive_statistics(df) -> Dict[str, any]:
    """
    This module contains functions to perform descriptive statistics on financial data from various sources
    Args:
        df: pd.DataFrame

    Returns: Dictionary of descriptive statistics

    """
    descriptive_statistics_df = {}
    #compute headline length
    df["headline_length"] = df["headline"].str.len()
    descriptive_statistics_df["headline_length"] = df["headline.length"].describe()
    #find number of articles with most active publisher
    active_publishers = df["publisher"].value_counts()
    descriptive_statistics_df["active_publishers"] = active_publishers
    #Analyze publication time to see trends
    df['date'] = pd.to_datetime(df['date'], utc=True)
    df['date_trend'] = df['date'].dt.date
    descriptive_statistics_df["date_counts"] = df['date_trend'].value_counts().sort_index()
    #Hour trend
    df['hour_trend'] = df['date'].dt.hour
    descriptive_statistics_df["time_counts"] = df['hour_trend'].value_counts().sort_index()

    return descriptive_statistics_df


def text_analysis(df):
    """
    This module contains functions to perform text analysis on financial data from various sources
    Args:
        df: pd.DataFrame

    Returns:

    """

