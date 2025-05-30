"""
eda_data.py - EDAda Processing functions for financial data analysis

This module contains functions to perform several EDA prcocess on financial data from various sources
for the nova-financial-solutions-week1 project.

Author: [Metasebiya Bizuneh]
Created: May 29, 2025
"""
import re
from typing import Dict
import pandas as pd
import load_data as ld
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from collections import Counter

def data_overview(df: pd.DataFrame):
    """
    This function is created to display data overview
    Args:
        df: pd.DataFrame

    Returns: Dictionary of data overview

    """
    result = {}
    result["info"] = df.info()
    result["type"] = df.dtypes
    result["shape"] = df.shape
    result["isnull"] = df.isnull().sum()

    return result


def descriptive_statistics(df):
    """
    This module contains functions to perform descriptive statistics on financial data from various sources
    Args:
        df: pd.DataFrame

    Returns: Dictionary of descriptive statistics

    """
    descriptive_statistics_df = {}
    #compute headline length
    df["headline_length"] = df["headline"].str.len()
    descriptive_statistics_df['headline_length'] = df["headline_length"].describe()
    #find number of articles with most active publisher
    active_publishers = df["publisher"].value_counts()
    descriptive_statistics_df['active_publishers'] = active_publishers.describe()
    #Analyze publication time to see trends
    df['date'] = pd.to_datetime(df['date'], format='mixed', utc=True)
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

    Returns: Dictionary of keywords/phrases and frequencies

    """

    # Initialize results dictionary
    results = {
        "noun_phrases": [],
        "nouns": [],
        "combined_keywords": [],
        "error_message": []
    }

    # Validate input
    if 'headline' not in df.columns:
        results["error_message"] = "DataFrame must contain a 'headline' column"
        return results

    # Initialize counters
    all_noun_phrases = []
    all_nouns = []
    error_rows = []

    # Process each headline
    for idx, headline in df['headline'].items():
        if not isinstance(headline, str) or not headline.strip():
            error_rows.append(idx)
            continue

        try:
            blob = TextBlob(headline)

            # --- Method 1: Extract Noun Phrases ---
            noun_phrases = blob.noun_phrases
            all_noun_phrases.extend(noun_phrases)

            # --- Method 2: Extract Nouns with POS Tagging ---
            pos_tags = blob.tags
            nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
            all_nouns.extend(nouns)

        except Exception as e:
            error_rows.append(idx)
            results["error_message"] = f"Error processing row(s) {error_rows}: {str(e)}"

    # Calculate frequencies
    noun_phrase_freq = Counter(all_noun_phrases)
    noun_freq = Counter(all_nouns)
    combined_keywords = all_noun_phrases + all_nouns
    combined_keyword_freq = Counter(combined_keywords)

    # Store results
    results["noun_phrases"] = [(phrase, freq) for phrase, freq in noun_phrase_freq.most_common()]
    results["nouns"] = [(noun, freq) for noun, freq in noun_freq.most_common()]
    results["combined_keywords"] = [(keyword, freq) for keyword, freq in combined_keyword_freq.most_common()]

    return results



def time_series_analysis(df):
    """
    Performs time series analysis by plotting article frequency over date and hour.

    Args:
        df (pd.DataFrame): DataFrame containing 'date_trend' and 'hour_trend' columns.

    Returns:
        object: each time frequency
    """
    # Ensure datetime and hour fields exist
    if 'date_trend' not in df or 'hour_trend' not in df:
        raise ValueError("Expected columns 'date_trend' and 'hour_trend' in DataFrame")

    df['day'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()

    daily_freq = df['date_trend'].value_counts().sort_index()
    hourly_freq = df['hour_trend'].value_counts().sort_index()
    day_freq = df['day'].value_counts().sort_index()
    month_freq = df['month'].value_counts().sort_index()

    return daily_freq, hourly_freq, day_freq, month_freq


def publisher_analysis(df):
    """
    Analyzes publishers by plotting article counts by publisher.

    Args:
        df (pd.DataFrame): DataFrame containing 'publisher' column.

    Returns:
        result: dictionary with keys 'publisher' and 'counts'
    """
    results = {}
    if 'publisher' not in df:
        raise ValueError("Expected column 'publisher' in DataFrame")

    #Top 10 publishers
    publisher_counts = df['publisher'].value_counts()
    top_publishers = publisher_counts.head(10)

    results["top_publishers"] = top_publishers

    #Publisher with email name
    email_publishers = df[df['publisher'].str.contains(r'@', na=False)]

    # Extract domain from email
    email_publishers['domain'] = email_publishers['publisher'].apply(
        lambda x: re.findall(r'@([\w.-]+)', x)[0] if '@' in x else None)

    # Count top contributing domains
    domain_counts = email_publishers['domain'].value_counts()
    top_domains = domain_counts.head(10)

    # count top publishers based on stock
    # Drop any missing values in 'publisher' or 'stock'
    df_filtered = df.dropna(subset=['publisher', 'stock'])

    # Group by stock and publisher, then count
    publisher_stock_counts = df_filtered.groupby(['stock', 'publisher']).size().reset_index(name='article_count')

    # View top 10 combinations
    top_combinations = publisher_stock_counts.sort_values(by='article_count', ascending=False).head(10)

    results["top_domains"] = top_domains

    return results
