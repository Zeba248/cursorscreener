from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import Stock
import yfinance as yf
import json
from datetime import datetime

def home(request):
    """Render the main stock screener page"""
    return render(request, 'stocks/index.html')

def stocks_json(request):
    """Return stock data as JSON"""
    # Get stocks from database
    stocks = Stock.objects.all()
    
    # If no stocks or data is old, fetch new data
    if not stocks or (stocks and stocks[0].last_updated < timezone.now() - timezone.timedelta(minutes=30)):
        update_stock_data()
        stocks = Stock.objects.all()
    
    # Convert to dictionary format
    stocks_data = []
    for stock in stocks:
        stocks_data.append({
            "ticker": stock.ticker,
            "name": stock.name,
            "sector": stock.sector,
            "price_change": stock.price_change,
            "rsi": stock.rsi,
            "volume": stock.volume,
            "market_cap": stock.market_cap,
            "is_positive": stock.is_positive
        })
    
    last_updated = stocks[0].last_updated.strftime("%Y-%m-%d %H:%M:%S") if stocks else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return JsonResponse({
        "last_updated": last_updated,
        "stocks": stocks_data
    })

def update_stock_data():
    """Update stock data from Yahoo Finance"""
    tickers = ['TSLA', 'AAPL', 'INFY.NS', 'RELIANCE.NS', 'TCS.NS']
    
    # Clear existing data
    Stock.objects.all().delete()
    
    for symbol in tickers:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            price_change = info.get("regularMarketChangePercent", 0)
            volume = info.get("volume")
            market_cap = info.get("marketCap")
            
            Stock.objects.create(
                ticker=symbol,
                name=info.get("shortName", symbol),
                sector=info.get("sector", "N/A"),
                price_change=round(price_change, 2),
                rsi=50,  # Dummy for now
                volume=f"{volume/1e6:.1f}M" if volume else "N/A",
                market_cap=f"${market_cap/1e9:.1f}B" if market_cap else "N/A",
                is_positive=price_change > 0
            )
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            # Create a placeholder entry
            Stock.objects.create(
                ticker=symbol,
                name=symbol,
                sector="N/A",
                price_change=0.0,
                rsi=50,
                volume="N/A",
                market_cap="N/A",
                is_positive=False
            )
