from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import Stock
import yfinance as yf
import json
from datetime import datetime, timedelta
import pandas as pd

def home(request):
    """Render the main stock screener page"""
    return render(request, 'stocks/index.html')

def stocks_json(request):
    """Return stock data as JSON with real-time updates"""
    # Get stocks from database
    stocks = Stock.objects.all()
    
    # Check if data needs updating (every 5 minutes for real-time feel)
    needs_update = not stocks or (stocks and stocks[0].last_updated < timezone.now() - timedelta(minutes=5))
    
    if needs_update:
        update_stock_data()
        stocks = Stock.objects.all()
    
    # Convert to dictionary format with comprehensive data
    stocks_data = []
    for stock in stocks:
        stocks_data.append({
            "ticker": stock.ticker,
            "name": stock.name,
            "sector": stock.sector,
            "current_price": stock.current_price,
            "previous_close": stock.previous_close,
            "price_change": stock.price_change,
            "price_change_percent": stock.price_change_percent,
            "market_cap": stock.market_cap,
            "volume": stock.volume,
            "avg_volume": stock.avg_volume,
            "day_high": stock.day_high,
            "day_low": stock.day_low,
            "fifty_two_week_high": stock.fifty_two_week_high,
            "fifty_two_week_low": stock.fifty_two_week_low,
            "pe_ratio": stock.pe_ratio,
            "dividend_yield": stock.dividend_yield,
            "beta": stock.beta,
            "eps": stock.eps,
            "rsi": stock.rsi,
            "is_positive": stock.is_positive,
            "market_state": stock.market_state
        })
    
    last_updated = stocks[0].last_updated.strftime("%Y-%m-%d %H:%M:%S") if stocks else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return JsonResponse({
        "last_updated": last_updated,
        "stocks": stocks_data,
        "total_stocks": len(stocks_data)
    })

def get_real_time_price(request, ticker):
    """Get real-time price for a specific ticker"""
    try:
        stock = yf.Ticker(ticker)
        # Get real-time data
        data = stock.history(period="1d", interval="1m")
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            return JsonResponse({
                "ticker": ticker,
                "current_price": round(current_price, 2),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            return JsonResponse({"error": "No data available"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def update_stock_data():
    """Update stock data from Yahoo Finance with comprehensive real-time information"""
    # Popular tickers from different markets
    tickers = [
        'AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN',  # US Tech
        'NVDA', 'META', 'NFLX', 'AMD', 'INTC',    # More US Tech
        'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS'  # Indian stocks
    ]
    
    # Clear existing data
    Stock.objects.all().delete()
    
    for symbol in tickers:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Get recent price data for more accurate current price
            hist = stock.history(period="2d")
            current_price = hist['Close'].iloc[-1] if not hist.empty else info.get("currentPrice", 0)
            previous_close = info.get("previousClose", current_price)
            
            # Calculate price changes
            price_change = current_price - previous_close
            price_change_percent = (price_change / previous_close * 100) if previous_close != 0 else 0
            
            # Format large numbers
            def format_large_number(value):
                if value is None:
                    return "N/A"
                if value >= 1e12:
                    return f"${value/1e12:.2f}T"
                elif value >= 1e9:
                    return f"${value/1e9:.2f}B"
                elif value >= 1e6:
                    return f"${value/1e6:.2f}M"
                else:
                    return f"${value:,.0f}"
            
            def format_volume(value):
                if value is None:
                    return "N/A"
                if value >= 1e9:
                    return f"{value/1e9:.2f}B"
                elif value >= 1e6:
                    return f"{value/1e6:.2f}M"
                elif value >= 1e3:
                    return f"{value/1e3:.2f}K"
                else:
                    return f"{value:,.0f}"
            
            Stock.objects.create(
                ticker=symbol,
                name=info.get("shortName", symbol),
                sector=info.get("sector", "N/A"),
                current_price=round(current_price, 2),
                previous_close=round(previous_close, 2),
                price_change=round(price_change, 2),
                price_change_percent=round(price_change_percent, 2),
                market_cap=format_large_number(info.get("marketCap")),
                volume=format_volume(info.get("volume")),
                avg_volume=format_volume(info.get("averageVolume")),
                day_high=round(info.get("dayHigh", 0), 2),
                day_low=round(info.get("dayLow", 0), 2),
                fifty_two_week_high=round(info.get("fiftyTwoWeekHigh", 0), 2),
                fifty_two_week_low=round(info.get("fiftyTwoWeekLow", 0), 2),
                pe_ratio=info.get("trailingPE"),
                dividend_yield=info.get("dividendYield"),
                beta=info.get("beta"),
                eps=info.get("trailingEps"),
                rsi=50,  # Would need additional calculation for real RSI
                is_positive=price_change > 0,
                market_state=info.get("marketState", "REGULAR")
            )
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            # Create a placeholder entry with minimal data
            Stock.objects.create(
                ticker=symbol,
                name=symbol,
                sector="N/A",
                current_price=0.0,
                previous_close=0.0,
                price_change=0.0,
                price_change_percent=0.0,
                market_cap="N/A",
                volume="N/A",
                avg_volume="N/A",
                day_high=0.0,
                day_low=0.0,
                fifty_two_week_high=0.0,
                fifty_two_week_low=0.0,
                rsi=50,
                is_positive=False,
                market_state="UNKNOWN"
            )
