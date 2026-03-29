"""
Data Fetcher Module

This module handles fetching stock data from yfinance API and processing it
with various calculated metrics including moving averages, returns, and volatility.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StockDataFetcher:
    """
    A class to fetch and process stock market data using yfinance.
    
    Attributes:
        symbol (str): The stock ticker symbol
        data (pd.DataFrame): The processed stock data
    """
    
    def __init__(self, symbol: str):
        """
        Initialize the StockDataFetcher with a stock symbol.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'INFY.NS', 'AAPL')
        """
        self.symbol = symbol.upper()
        self.data: Optional[pd.DataFrame] = None
        self._raw_data: Optional[pd.DataFrame] = None
    
    async def fetch_data(self, period: str = "1y") -> pd.DataFrame:
        """
        Fetch stock data from yfinance for the specified period.
        
        Args:
            period: Time period for data fetching (default: '1y' for 1 year)
        
        Returns:
            DataFrame with raw stock data
            
        Raises:
            ValueError: If no data is found for the symbol
        """
        try:
            logger.info(f"Fetching data for {self.symbol}")
            ticker = yf.Ticker(self.symbol)
            self._raw_data = ticker.history(period=period)
            
            if self._raw_data.empty:
                raise ValueError(f"No data found for symbol: {self.symbol}")
            
            logger.info(f"Successfully fetched {len(self._raw_data)} records for {self.symbol}")
            return self._raw_data
            
        except Exception as e:
            logger.error(f"Error fetching data for {self.symbol}: {str(e)}")
            raise
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean the raw stock data by handling missing values and formatting.
        
        Returns:
            Cleaned DataFrame
            
        Raises:
            ValueError: If no raw data is available
        """
        if self._raw_data is None or self._raw_data.empty:
            raise ValueError("No raw data available. Call fetch_data() first.")
        
        df = self._raw_data.copy()
        
        # Reset index to make Date a column
        df = df.reset_index()
        
        # Rename columns for consistency
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        # Handle missing values
        # Forward fill for price data (use previous day's value)
        price_columns = ['open', 'high', 'low', 'close']
        for col in price_columns:
            if col in df.columns:
                df[col] = df[col].ffill()
        
        # Fill volume with 0 if missing
        if 'volume' in df.columns:
            df['volume'] = df['volume'].fillna(0)
        
        # Drop any remaining rows with NaN in critical columns
        df = df.dropna(subset=['open', 'high', 'low', 'close'])
        
        # Ensure proper data types
        df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
        
        for col in price_columns:
            df[col] = df[col].astype(float)
        
        if 'volume' in df.columns:
            df['volume'] = df['volume'].astype(int)
        
        logger.info(f"Data cleaned. Records: {len(df)}")
        return df
    
    def add_calculated_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add calculated metrics to the stock data.
        
        Calculated fields:
        - daily_return: (Close - Open) / Open
        - ma_7: 7-day moving average of closing price
        - high_52w: 52-week high
        - low_52w: 52-week low
        - volatility: Rolling standard deviation of returns (20-day window)
        
        Args:
            df: Cleaned stock data DataFrame
            
        Returns:
            DataFrame with additional calculated fields
        """
        df = df.copy()
        
        # Daily Return = (Close - Open) / Open
        df['daily_return'] = (df['close'] - df['open']) / df['open']
        
        # 7-day Moving Average
        df['ma_7'] = df['close'].rolling(window=7, min_periods=1).mean()
        
        # 20-day Moving Average (for trend analysis)
        df['ma_20'] = df['close'].rolling(window=20, min_periods=1).mean()
        
        # 52-week High and Low (rolling)
        # Using 252 trading days as approximation for 52 weeks
        trading_days_year = min(252, len(df))
        df['high_52w'] = df['high'].rolling(window=trading_days_year, min_periods=1).max()
        df['low_52w'] = df['low'].rolling(window=trading_days_year, min_periods=1).min()
        
        # Volatility (rolling standard deviation of daily returns, 20-day window)
        df['volatility'] = df['daily_return'].rolling(window=20, min_periods=1).std()
        
        # Annualized volatility
        df['volatility_annualized'] = df['volatility'] * np.sqrt(252)
        
        # Price change from previous day
        df['price_change'] = df['close'].diff()
        df['price_change_pct'] = df['close'].pct_change() * 100
        
        logger.info("Calculated fields added successfully")
        return df
    
    async def process(self) -> pd.DataFrame:
        """
        Execute the full data processing pipeline.
        
        Returns:
            Fully processed DataFrame with all calculated fields
        """
        await self.fetch_data()
        df = self.clean_data()
        self.data = self.add_calculated_fields(df)
        return self.data
    
    def get_last_n_days(self, n: int = 30) -> pd.DataFrame:
        """
        Get the last N days of processed data.
        
        Args:
            n: Number of days to return (default: 30)
            
        Returns:
            DataFrame with last N days of data
            
        Raises:
            ValueError: If no processed data is available
        """
        if self.data is None:
            raise ValueError("No processed data available. Call process() first.")
        
        return self.data.tail(n).copy()
    
    def get_summary_stats(self) -> dict:
        """
        Calculate summary statistics for the stock.
        
        Returns:
            Dictionary containing summary statistics
        """
        if self.data is None:
            raise ValueError("No processed data available. Call process() first.")
        
        df = self.data
        latest = df.iloc[-1]
        
        return {
            "symbol": self.symbol,
            "latest_date": latest['date'].strftime('%Y-%m-%d'),
            "latest_close": round(latest['close'], 2),
            "high_52w": round(df['high'].max(), 2),
            "low_52w": round(df['low'].min(), 2),
            "avg_close": round(df['close'].mean(), 2),
            "avg_volume": int(df['volume'].mean()),
            "volatility": round(latest['volatility'], 6),
            "volatility_annualized": round(latest['volatility_annualized'], 4),
            "total_return": round(
                (df.iloc[-1]['close'] - df.iloc[0]['close']) / df.iloc[0]['close'] * 100, 2
            ),
            "avg_daily_return": round(df['daily_return'].mean() * 100, 4),
        }


async def fetch_and_process_stock(symbol: str) -> Tuple[pd.DataFrame, dict]:
    """
    Convenience function to fetch and process stock data.
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        Tuple of (processed DataFrame, summary statistics dict)
    """
    fetcher = StockDataFetcher(symbol)
    data = await fetcher.process()
    summary = fetcher.get_summary_stats()
    return data, summary


def compare_stocks(df1: pd.DataFrame, df2: pd.DataFrame, 
                   symbol1: str, symbol2: str) -> dict:
    """
    Compare two stocks based on various metrics.
    
    Args:
        df1: Processed data for first stock
        df2: Processed data for second stock
        symbol1: Symbol of first stock
        symbol2: Symbol of second stock
        
    Returns:
        Dictionary containing comparison metrics
    """
    # Align data by date for correlation calculation
    merged = pd.merge(
        df1[['date', 'close', 'daily_return']].rename(
            columns={'close': 'close_1', 'daily_return': 'return_1'}
        ),
        df2[['date', 'close', 'daily_return']].rename(
            columns={'close': 'close_2', 'daily_return': 'return_2'}
        ),
        on='date',
        how='inner'
    )
    
    # Calculate correlation
    correlation = merged['return_1'].corr(merged['return_2'])
    
    return {
        "symbol1": symbol1,
        "symbol2": symbol2,
        "comparison_period_days": len(merged),
        "metrics": {
            symbol1: {
                "avg_return": round(df1['daily_return'].mean() * 100, 4),
                "volatility": round(df1['volatility'].iloc[-1], 6),
                "total_return": round(
                    (df1.iloc[-1]['close'] - df1.iloc[0]['close']) / df1.iloc[0]['close'] * 100, 2
                )
            },
            symbol2: {
                "avg_return": round(df2['daily_return'].mean() * 100, 4),
                "volatility": round(df2['volatility'].iloc[-1], 6),
                "total_return": round(
                    (df2.iloc[-1]['close'] - df2.iloc[0]['close']) / df2.iloc[0]['close'] * 100, 2
                )
            }
        },
        "correlation": round(correlation, 4) if not np.isnan(correlation) else None,
        "correlation_interpretation": _interpret_correlation(correlation)
    }


def _interpret_correlation(corr: float) -> str:
    """Interpret correlation coefficient value."""
    if np.isnan(corr):
        return "Unable to calculate"
    elif corr >= 0.7:
        return "Strong positive correlation"
    elif corr >= 0.3:
        return "Moderate positive correlation"
    elif corr >= -0.3:
        return "Weak or no correlation"
    elif corr >= -0.7:
        return "Moderate negative correlation"
    else:
        return "Strong negative correlation"
