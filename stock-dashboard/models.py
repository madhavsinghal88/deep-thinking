"""
Pydantic Models Module

This module defines Pydantic models for request/response validation
and API documentation in the FastAPI application.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date


class CompanyInfo(BaseModel):
    """Model for company information."""
    
    symbol: str = Field(..., description="Stock ticker symbol")
    name: str = Field(..., description="Company name")
    sector: str = Field(..., description="Business sector")
    exchange: str = Field(..., description="Stock exchange")
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "INFY.NS",
                "name": "Infosys Limited",
                "sector": "Information Technology",
                "exchange": "NSE"
            }
        }


class StockDataPoint(BaseModel):
    """Model for a single day's stock data."""
    
    date: str = Field(..., description="Trading date")
    open: float = Field(..., description="Opening price")
    high: float = Field(..., description="Day's high price")
    low: float = Field(..., description="Day's low price")
    close: float = Field(..., description="Closing price")
    volume: int = Field(..., description="Trading volume")
    daily_return: Optional[float] = Field(None, description="Daily return percentage")
    ma_7: Optional[float] = Field(None, description="7-day moving average")
    ma_20: Optional[float] = Field(None, description="20-day moving average")
    high_52w: Optional[float] = Field(None, description="52-week high")
    low_52w: Optional[float] = Field(None, description="52-week low")
    volatility: Optional[float] = Field(None, description="Rolling volatility")
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-01-15",
                "open": 1450.50,
                "high": 1465.00,
                "low": 1445.25,
                "close": 1460.75,
                "volume": 5000000,
                "daily_return": 0.0071,
                "ma_7": 1455.50,
                "ma_20": 1440.25,
                "high_52w": 1520.00,
                "low_52w": 1200.00,
                "volatility": 0.0125
            }
        }


class StockDataResponse(BaseModel):
    """Response model for stock data endpoint."""
    
    symbol: str = Field(..., description="Stock ticker symbol")
    company_name: str = Field(..., description="Company name")
    data_points: int = Field(..., description="Number of data points returned")
    period: str = Field(..., description="Data period description")
    data: List[StockDataPoint] = Field(..., description="List of stock data points")
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "INFY.NS",
                "company_name": "Infosys Limited",
                "data_points": 30,
                "period": "Last 30 days",
                "data": []
            }
        }


class HealthScoreComponents(BaseModel):
    """Model for health score component breakdown."""
    
    return_score: float = Field(..., description="Score based on average returns (0-25)")
    volatility_score: float = Field(..., description="Score based on volatility (0-25)")
    trend_score: float = Field(..., description="Score based on price trend (0-25)")
    position_score: float = Field(..., description="Score based on position vs 52w high (0-25)")


class HealthScore(BaseModel):
    """Model for stock health score."""
    
    total_score: float = Field(..., description="Overall health score (0-100)")
    category: str = Field(..., description="Health category (Excellent/Good/Fair/Poor/Critical)")
    description: str = Field(..., description="Human-readable description")
    components: HealthScoreComponents = Field(..., description="Score breakdown")
    max_possible: int = Field(100, description="Maximum possible score")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_score": 72.5,
                "category": "Good",
                "description": "Solid performance with acceptable risk levels",
                "components": {
                    "return_score": 18.5,
                    "volatility_score": 20.0,
                    "trend_score": 16.5,
                    "position_score": 17.5
                },
                "max_possible": 100
            }
        }


class StockSummary(BaseModel):
    """Model for stock summary statistics."""
    
    symbol: str = Field(..., description="Stock ticker symbol")
    company_name: str = Field(..., description="Company name")
    latest_date: str = Field(..., description="Date of latest data")
    latest_close: float = Field(..., description="Latest closing price")
    high_52w: float = Field(..., description="52-week high price")
    low_52w: float = Field(..., description="52-week low price")
    avg_close: float = Field(..., description="Average closing price")
    avg_volume: int = Field(..., description="Average trading volume")
    volatility: float = Field(..., description="Current volatility")
    volatility_annualized: float = Field(..., description="Annualized volatility")
    total_return: float = Field(..., description="Total return over period (%)")
    avg_daily_return: float = Field(..., description="Average daily return (%)")
    health_score: HealthScore = Field(..., description="Stock health score")
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "INFY.NS",
                "company_name": "Infosys Limited",
                "latest_date": "2024-01-15",
                "latest_close": 1460.75,
                "high_52w": 1520.00,
                "low_52w": 1200.00,
                "avg_close": 1380.50,
                "avg_volume": 4500000,
                "volatility": 0.0125,
                "volatility_annualized": 0.1984,
                "total_return": 15.5,
                "avg_daily_return": 0.05,
                "health_score": {}
            }
        }


class ComparisonMetrics(BaseModel):
    """Model for single stock metrics in comparison."""
    
    avg_return: float = Field(..., description="Average daily return (%)")
    volatility: float = Field(..., description="Current volatility")
    total_return: float = Field(..., description="Total return over period (%)")


class StockComparison(BaseModel):
    """Response model for stock comparison endpoint."""
    
    symbol1: str = Field(..., description="First stock symbol")
    symbol2: str = Field(..., description="Second stock symbol")
    comparison_period_days: int = Field(..., description="Number of overlapping days compared")
    metrics: Dict[str, ComparisonMetrics] = Field(..., description="Metrics for each stock")
    correlation: Optional[float] = Field(None, description="Price correlation coefficient")
    correlation_interpretation: str = Field(..., description="Human-readable correlation description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol1": "INFY.NS",
                "symbol2": "TCS.NS",
                "comparison_period_days": 250,
                "metrics": {
                    "INFY.NS": {
                        "avg_return": 0.05,
                        "volatility": 0.0125,
                        "total_return": 15.5
                    },
                    "TCS.NS": {
                        "avg_return": 0.04,
                        "volatility": 0.0110,
                        "total_return": 12.3
                    }
                },
                "correlation": 0.75,
                "correlation_interpretation": "Strong positive correlation"
            }
        }


class ErrorResponse(BaseModel):
    """Model for error responses."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    symbol: Optional[str] = Field(None, description="Related symbol if applicable")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "NotFound",
                "message": "Stock symbol not found or not supported",
                "symbol": "INVALID.NS"
            }
        }


class CacheInfo(BaseModel):
    """Model for cache information."""
    
    symbol: str = Field(..., description="Stock symbol")
    last_updated: str = Field(..., description="Last update timestamp")
    record_count: int = Field(..., description="Number of cached records")
    data_start_date: str = Field(..., description="Start date of cached data")
    data_end_date: str = Field(..., description="End date of cached data")


class MarketStatus(BaseModel):
    """Model for market status information."""
    
    status: str = Field(..., description="Market status (open/closed)")
    message: str = Field(..., description="Status message")
    current_time: str = Field(..., description="Current server time")
    timezone: str = Field(..., description="Timezone")


class SearchResult(BaseModel):
    """Model for stock search results."""
    
    symbol: str = Field(..., description="Stock ticker symbol")
    name: str = Field(..., description="Company/Security name")
    exchange: str = Field(..., description="Stock exchange")
    type: str = Field(default="EQUITY", description="Security type (EQUITY, ETF, etc.)")
    score: Optional[float] = Field(None, description="Search relevance score")
    sector: Optional[str] = Field(None, description="Standardized sector name")
    sector_color: Optional[str] = Field(None, description="Sector display color (hex)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "exchange": "NASDAQ",
                "type": "EQUITY",
                "score": 100000,
                "sector": "Technology",
                "sector_color": "#00d4ff"
            }
        }


class SectorInfo(BaseModel):
    """Model for sector information."""
    
    name: str = Field(..., description="Standardized sector name")
    color: str = Field(..., description="Display color (hex)")
    icon: str = Field(..., description="Display icon/emoji")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Technology",
                "color": "#00d4ff",
                "icon": "💻"
            }
        }
