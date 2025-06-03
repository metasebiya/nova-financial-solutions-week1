import pandas as pd

class DataCleaner:
    def __init__(self, dataframe=None):
        self.df = dataframe.copy() if dataframe is not None else pd.DataFrame()

    def clean_news_data(self):
        # ... (existing method from Task 1) ...
        if 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce').dt.floor('D')
            self.df.dropna(subset=['date'], inplace=True)
        if 'headline' in self.df.columns:
            self.df.dropna(subset=['headline'], inplace=True)
            self.df['headline'] = self.df['headline'].astype(str).str.strip().str.lower()
        print("News data cleaning complete.")
        return self.df

    def clean_stock_data(self):
        """
        Performs cleaning on a single stock price DataFrame.
        Assumes 'Date' is already the index and is datetime.
        Ensures numerical columns are numeric.
        """
        # Data loading now handles Date as index and initial conversion
        # This method can focus on ensuring data types and handling any remaining NaNs
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        # Drop rows where critical price/volume data might be missing after conversion
        self.df.dropna(subset=['Close', 'Volume'], inplace=True) 
        
        print("Stock data cleaning complete.")
        return self.df

    def prepare_for_merge(self, news_df, stock_df):
        # ... (existing method from Task 3) ...
        news_df['date'] = news_df['date'].dt.normalize()
        stock_df.index = stock_df.index.normalize()
        return news_df, stock_df