import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Visualizer:
    def __init__(self, data_for_plotting=None):
        self.data = data_for_plotting
        sns.set_style("whitegrid") # Set a nice style for plots

    def plot_stock_prices_with_indicators(self, dataframe, stock_symbol, indicators=['SMA_20', 'RSI']):
        """
        Plots stock closing prices along with selected technical indicators.
        """
        if 'Close' not in dataframe.columns:
            print("Error: 'Close' column not found in DataFrame.")
            return

        plt.figure(figsize=(15, 8))

        # Plot Close Price
        plt.subplot(2, 1, 1)
        plt.plot(dataframe.index, dataframe['Close'], label='Close Price', color='blue', alpha=0.7)
        for indicator in indicators:
            if indicator in dataframe.columns and 'SMA' in indicator:
                plt.plot(dataframe.index, dataframe[indicator], label=indicator, linestyle='--')
        plt.title(f'{stock_symbol} Stock Price and Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)

        # Plot other indicators (e.g., RSI, MACD) in a separate subplot
        if 'RSI' in indicators and 'RSI' in dataframe.columns:
            plt.subplot(2, 1, 2)
            plt.plot(dataframe.index, dataframe['RSI'], label='RSI', color='purple')
            plt.axhline(70, color='red', linestyle='--', alpha=0.6, label='Overbought (70)')
            plt.axhline(30, color='green', linestyle='--', alpha=0.6, label='Oversold (30)')
            plt.title(f'{stock_symbol} Relative Strength Index (RSI)')
            plt.xlabel('Date')
            plt.ylabel('RSI Value')
            plt.legend()
            plt.grid(True)
        elif 'MACD' in indicators and 'MACD' in dataframe.columns:
            plt.subplot(2, 1, 2)
            plt.plot(dataframe.index, dataframe['MACD'], label='MACD', color='orange')
            plt.plot(dataframe.index, dataframe['MACD_Signal'], label='Signal Line', color='red', linestyle=':')
            plt.bar(dataframe.index, dataframe['MACD_Hist'], label='Histogram', color='grey', alpha=0.6)
            plt.title(f'{stock_symbol} MACD Indicator')
            plt.xlabel('Date')
            plt.ylabel('MACD Value')
            plt.legend()
            plt.grid(True)

        plt.tight_layout()
        plt.show()
        plt.close()
       
    def plot_histogram(self, data_series, title, xlabel, ylabel='Frequency', bins=30):
        """
        Plots a histogram for numerical data.
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(data_series, bins=bins, kde=True)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.show()

    def plot_bar_chart(self, data_series, title, xlabel, ylabel='Count', top_n=None):
        """
        Plots a bar chart for categorical data.
        """
        plt.figure(figsize=(12, 7))
        if top_n:
            data_series = data_series.head(top_n)
        sns.barplot(x=data_series.index, y=data_series.values, palette='viridis')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def plot_time_series(self, data_series, title, xlabel='Date', ylabel='Frequency'):
        """
        Plots a time series.
        """
        plt.figure(figsize=(14, 7))
        data_series.plot(kind='line', marker='o', linestyle='-')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_sentiment_distribution(self, sentiment_counts, title="Sentiment Distribution"):
        """
        Plots the distribution of sentiment categories.
        """
        plt.figure(figsize=(8, 6))
        sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='coolwarm')
        plt.title(title)
        plt.xlabel("Sentiment Category")
        plt.ylabel("Number of Articles")
        plt.tight_layout()
        plt.show()

    def plot_top_keywords(self, keywords_data, title="Top Common Keywords"):
        """
        Plots the top common keywords.
        Args:
            keywords_data (list): List of (keyword, count) tuples.
        """
        if not keywords_data:
            print("No keyword data to plot.")
            return

        keywords, counts = zip(*keywords_data)
        plt.figure(figsize=(12, 7))
        sns.barplot(x=list(keywords), y=list(counts), palette='plasma')
        plt.title(title)
        plt.xlabel("Keywords")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def plot_hourly_distribution(self, hourly_counts, title="Hourly News Publication Distribution"):
        """
        Plots the distribution of news publications by hour of the day.
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(x=hourly_counts.index, y=hourly_counts.values, palette='mako')
        plt.title(title)
        plt.xlabel("Hour of Day (UTC-4)")
        plt.ylabel("Number of Articles")
        plt.xticks(range(0, 24))
        plt.tight_layout()
        plt.show()

        if 'Close' not in dataframe.columns:
            print("Error: 'Close' column not found in DataFrame.")
            return

        plt.figure(figsize=(15, 8))

        # Plot Close Price
        plt.subplot(2, 1, 1) # Two rows, one column, first plot
        plt.plot(dataframe.index, dataframe['Close'], label='Close Price', color='blue', alpha=0.7)
        for indicator in indicators:
            if indicator in dataframe.columns and 'SMA' in indicator:
                plt.plot(dataframe.index, dataframe[indicator], label=indicator, linestyle='--')
        plt.title(f'{stock_symbol} Stock Price and Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)

        # Plot other indicators (e.g., RSI, MACD) in a separate subplot
        if 'RSI' in indicators and 'RSI' in dataframe.columns:
            plt.subplot(2, 1, 2)
            plt.plot(dataframe.index, dataframe['RSI'], label='RSI', color='purple')
            plt.axhline(70, color='red', linestyle='--', alpha=0.6, label='Overbought (70)')
            plt.axhline(30, color='green', linestyle='--', alpha=0.6, label='Oversold (30)')
            plt.title(f'{stock_symbol} Relative Strength Index (RSI)')
            plt.xlabel('Date')
            plt.ylabel('RSI Value')
            plt.legend()
            plt.grid(True)
        elif 'MACD' in indicators and 'MACD' in dataframe.columns:
            plt.subplot(2, 1, 2)
            plt.plot(dataframe.index, dataframe['MACD'], label='MACD', color='orange')
            plt.plot(dataframe.index, dataframe['MACD_Signal'], label='Signal Line', color='red', linestyle=':')
            plt.bar(dataframe.index, dataframe['MACD_Hist'], label='Histogram', color='grey', alpha=0.6)
            plt.title(f'{stock_symbol} MACD Indicator')
            plt.xlabel('Date')
            plt.ylabel('MACD Value')
            plt.legend()
            plt.grid(True)

        plt.tight_layout()
        plt.show()

    def plot_sentiment_vs_returns_scatter(self, df_merged, title="Average Daily Sentiment vs. Daily Stock Returns"):
        """
        Plots a scatter plot of average daily sentiment against daily stock returns.
        """
        
        if 'Avg_Daily_Sentiment' not in df_merged.columns or 'Daily_Return' not in df_merged.columns:
            print("Error: Required columns not found for scatter plot.")
            return

        plt.figure(figsize=(10, 7))
        sns.scatterplot(x='Avg_Daily_Sentiment', y='Daily_Return', data=df_merged, alpha=0.6)
        plt.title(title)
        plt.xlabel("Average Daily News Sentiment Score")
        plt.ylabel("Daily Stock Return (%)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        plt.close() # Add this line to close the figure

    def plot_correlation_heatmap(self, df_merged, columns, title="Correlation Heatmap"):
        """
        Plots a correlation heatmap for selected columns.
        """
        if not all(col in df_merged.columns for col in columns):
            print("Error: One or more specified columns not found for heatmap.")
            return

        correlation_matrix = df_merged[columns].corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
        plt.title(title)
        plt.tight_layout()
        plt.show()
        plt.close() 