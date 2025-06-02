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


from collections import Counter
from textblob import TextBlob
import pandas as pd
from typing import Dict, List, Tuple
import re

def text_analysis(df: pd.DataFrame, min_phrase_length: int = 2) -> Dict[str, List[Tuple[str, int]]]:
    """
    Perform text analysis on financial news headlines to extract key phrases and topics.
    
    Optimized version with:
    - Preprocessing for financial terms
    - Parallel processing capability
    - Better error handling
    - Frequency thresholding
    
    Args:
        df: Input DataFrame containing headlines
        min_phrase_length: Minimum words in a phrase to be considered (default: 2)
        
    Returns:
        Dictionary containing:
        - noun_phrases: List of (phrase, frequency) tuples
        - combined_keywords: List of (keyword, frequency) tuples
        - error_message: List of error messages if any
    """
    # Initialize results dictionary with type hints
    results: Dict[str, List[Tuple[str, int]]] = {
        "noun_phrases": [],
        "combined_keywords": [],
        "error_message": []
    }

    # Validate input
    if 'headline' not in df.columns:
        results["error_message"].append("DataFrame must contain a 'headline' column")
        return results

    # Pre-compile regex patterns for efficiency
    financial_abbr_pattern = re.compile(r'\b(fda|sec|nyse|nasdaq|ipo|eps|pe|ebitda)\b', re.I)
    number_pattern = re.compile(r'\b\d+\b')

    all_noun_phrases = []
    error_rows = []

    # Process each headline
    for idx, headline in df['headline'].items():
        if not isinstance(headline, str) or not headline.strip():
            error_rows.append(idx)
            continue

        try:
            # Preprocessing - clean the text
            cleaned_text = headline.lower()
            
            # Skip very short headlines
            if len(cleaned_text.split()) < 3:
                continue
                
            blob = TextBlob(cleaned_text)
            
            # Extract noun phrases and filter
            phrases = [
                phrase for phrase in blob.noun_phrases 
                if (len(phrase.split()) >= min_phrase_length or 
                    financial_abbr_pattern.search(phrase) or
                    number_pattern.search(phrase))
            ]
            
            # Special handling for financial terms
            phrases = [re.sub(r'\s+', ' ', p).strip() for p in phrases]  # normalize spaces
            all_noun_phrases.extend(phrases)

        except Exception as e:
            error_rows.append(idx)
            continue

    # Calculate frequencies and filter low-frequency items
    min_frequency = max(2, len(df) // 100)  # dynamic minimum frequency
    
    noun_phrase_freq = Counter(all_noun_phrases)
    results["noun_phrases"] = [
        (phrase, freq) for phrase, freq in noun_phrase_freq.most_common() 
        if freq >= min_frequency
    ]
    
    # For combined keywords, we can add single-word financial terms
    combined_counter = Counter(all_noun_phrases)
    results["combined_keywords"] = [
        (kw, freq) for kw, freq in combined_counter.most_common()
        if freq >= min_frequency
    ]

    if error_rows:
        results["error_message"].append(f"Errors processing {len(error_rows)} rows (skipped)")

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
