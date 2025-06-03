import pandas as pd

class CorrelationAnalyzer:
    def __init__(self, news_df):
        self.news_df = news_df.copy()
        # Stock_dfs will be passed when calling analyze_multiple_stocks
        self.stock_dfs = {} 

    def align_and_merge_data(self, stock_df):
        """
        Aligns news and a single stock's data by date and merges them.
        Assumes 'date' in news_df is normalized and stock_df has 'Daily_Return' and 'sentiment_score'.
        Args:
            stock_df (pd.DataFrame): Cleaned stock DataFrame for a single ticker, with 'Daily_Return'.
        Returns:
            pd.DataFrame: Merged DataFrame ready for correlation analysis for this stock.
        """
        # Ensure news_df has sentiment_score and 'date' column
        if 'sentiment_score' not in self.news_df.columns:
            print("Error: 'sentiment_score' column not found in news_df. Please run sentiment analysis first.")
            return None
        if 'date' not in self.news_df.columns:
            print("Error: 'date' column not found in news_df.")
            return None
        
        # Aggregate sentiment scores for each day if multiple articles exist
        daily_sentiment = self.news_df.groupby(self.news_df['date'])['sentiment_score'].mean().reset_index()
        daily_sentiment.rename(columns={'date': 'Date', 'sentiment_score': 'Avg_Daily_Sentiment'}, inplace=True)
        
        # Ensure stock_df has 'Daily_Return' and its index is the 'Date'
        if 'Daily_Return' not in stock_df.columns:
            print("Error: 'Daily_Return' column not found in stock_df. Please calculate daily returns first.")
            return None
        if not isinstance(stock_df.index, pd.DatetimeIndex):
             print("Error: Stock DataFrame index is not datetime.")
             return None
        
        # Ensure stock_df index is normalized to daily for clean merge
        stock_df_copy = stock_df.copy() # Work on a copy
        stock_df_copy.index = stock_df_copy.index.normalize()


        # Merge based on Date
        merged_df = pd.merge(
            daily_sentiment,
            stock_df_copy[['Daily_Return']], # Select only 'Daily_Return' for merging
            left_on='Date',
            right_index=True,
            how='inner' # Only keep dates where both news and stock data are available
        )
        merged_df.dropna(subset=['Avg_Daily_Sentiment', 'Daily_Return'], inplace=True) # Drop NaNs if any
        print(f"News sentiment and stock data aligned and merged for {stock_df.name if stock_df.name else 'a stock'}.")
        return merged_df

    def calculate_correlation(self, df_merged):
        """
        Calculates the Pearson correlation coefficient between average daily sentiment and stock returns.
        Args:
            df_merged (pd.DataFrame): Merged DataFrame containing 'Avg_Daily_Sentiment' and 'Daily_Return'.
        Returns:
            float: Pearson correlation coefficient.
        """
        if df_merged is None or 'Avg_Daily_Sentiment' not in df_merged.columns or 'Daily_Return' not in df_merged.columns:
            print("Error: Merged DataFrame is not suitable for correlation calculation.")
            return None
        
        correlation = df_merged['Avg_Daily_Sentiment'].corr(df_merged['Daily_Return'])
        print(f"Pearson Correlation between Avg_Daily_Sentiment and Daily_Return: {correlation:.4f}")
        return correlation

    def analyze_multiple_stocks(self, all_stock_dfs):
        """
        Analyzes correlation for multiple stocks.
        Args:
            all_stock_dfs (dict): Dictionary of stock DataFrames, each with 'Daily_Return' calculated.
        Returns:
            dict: A dictionary of {ticker: correlation_coefficient}.
        """
        all_correlations = {}
        for ticker, stock_df in all_stock_dfs.items():
            print(f"\n--- Analyzing Correlation for {ticker} ---")
            # Ensure stock_df has a name (ticker) for better logging
            stock_df.name = ticker 

            merged_df = self.align_and_merge_data(stock_df)
            if merged_df is not None and not merged_df.empty:
                correlation = self.calculate_correlation(merged_df)
                all_correlations[ticker] = correlation
            else:
                print(f"Could not merge data for {ticker}. Skipping correlation.")
        return all_correlations