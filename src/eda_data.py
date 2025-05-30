"""
eda_data.py - EDAda Processing functions for financial data analysis

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
    #df["headline_length"] = df["headline"].str.len()
    descriptive_statistics_df["headline_length"] = df["headline"].str.len()
    #find number of articles with most active publisher
    active_publishers = df["publisher"].value_counts()
    descriptive_statistics_df["active_publishers"] = active_publishers
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
    # result = { }
    # blob = TextBlob(df["headline"])
    # # --- Method 1: Extract Noun Phrases ---
    # noun_phrases = blob.noun_phrases
    # print("Noun Phrases:")
    # for phrase in noun_phrases:
    #     print(f"- {phrase}")
    #
    # # --- Method 2: Extract Keywords (Nouns) with POS Tagging ---
    # words = blob.words  # Tokenize into words
    # pos_tags = blob.tags  # Get POS tags
    # nouns = [word for word, pos in pos_tags if pos.startswith('NN')]  # Filter nouns
    # noun_freq = Counter(nouns)
    #
    # print("\nTop 5 Nouns (Frequency-Based):")
    # for word, freq in noun_freq.most_common(5):
    #     print(f"- {word}: {freq}")
    #
    # # --- Method 3: Combine Noun Phrases and Nouns ---
    # all_keywords = noun_phrases + nouns
    # keyword_freq = Counter(all_keywords)
    #
    # print("\nTop 5 Keywords/Phrases (Combined):")
    # for keyword, freq in keyword_freq.most_common(5):
    #     result["keywords"] = keyword
    #     result["frequency"] = freq
    #     print(f"- {keyword}: {freq}")
    #
    # return result
    # Initialize results dictionary
    results = {
        "noun_phrases": [],
        "nouns": [],
        "combined_keywords": [],
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

    # Print top 5 for each category
    print("Top 5 Noun Phrases:")
    for phrase, freq in results["noun_phrases"][:5]:
        print(f"- {phrase}: {freq}")

    print("\nTop 5 Nouns:")
    for noun, freq in results["nouns"][:5]:
        print(f"- {noun}: {freq}")

    print("\nTop 5 Combined Keywords/Phrases:")
    for keyword, freq in results["combined_keywords"][:5]:
        print(f"- {keyword}: {freq}")

    return results



def time_series_analysis(df):
    """
    This function performs a time series analysis on financial data from various sources
    Args:
        df: pd.DataFrame

    Returns: plots of time series analysis

    """
    # Plot 1: Frequency over date
    fig1, ax1 = plt.subplots()
    df['date_trend'].value_counts().sort_index().plot(kind='line', ax=ax1,title='Article Publication Frequency Over Date')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number of Articles')

    # Plot 2: Frequency over hour
    fig2, ax2 = plt.subplots()
    df['hour_trend'].hist(bins=24, ax=ax2,title='Article Publication Frequency Over Time')
    ax2.set_xlabel('Hour')
    ax2.set_ylabel('Number of Articles')

    return fig1, fig2

def publisher_analysis(df):
    """
    This function performs a publisher analysis on financial data from various sources
    Args:
        df: pd.DataFrame

    Returns:

    """
    # Plot1: Distribution of publication of news feeds
    fig1, ax1 = plt.subplots()
    df['publisher'].value_counts().hist(bins=24, ax=ax1, title='Publishers Over news feeds')
    ax1.set_xlabel('Count')
    ax1.set_ylabel('Number of Articles')

    # Plot2: Distribution of publication over stock type
    fig2, ax2 = plt.subplots()
    df['publisher'].value_counts().hist(bins=24, ax=ax2, title='Publishers Over news feeds')
    ax2.set_xlabel('Count')
    ax2.set_ylabel('Number of Articles')

    return fig1
