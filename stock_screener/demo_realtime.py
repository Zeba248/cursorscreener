#!/usr/bin/env python3
"""
Real-time Stock Data Demo Script
This script demonstrates the real-time stock data integration with yfinance
"""

import os
import sys
import django
import time
from datetime import datetime

# Setup Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_screener.settings')
django.setup()

from stocks.models import Stock
from stocks.views import update_stock_data

def display_stock_summary():
    """Display a summary of all stocks with real-time data"""
    stocks = Stock.objects.all().order_by('-price_change_percent')
    
    print("\n" + "="*80)
    print("🚀 REAL-TIME STOCK MARKET DATA - YFINANCE INTEGRATION")
    print("="*80)
    print(f"📊 Total Stocks Tracked: {stocks.count()}")
    print(f"🕐 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Display header
    print(f"{'SYMBOL':<12} {'COMPANY':<25} {'PRICE':<12} {'CHANGE':<12} {'MKT CAP':<15} {'P/E':<8}")
    print("-"*80)
    
    for stock in stocks:
        symbol = stock.ticker[:11]
        name = stock.name[:24] if stock.name else "N/A"
        price = f"${stock.current_price:.2f}"
        change_color = "🟢" if stock.is_positive else "🔴"
        change = f"{change_color} {stock.price_change_percent:+.2f}%"
        market_cap = stock.market_cap[:14]
        pe_ratio = f"{stock.pe_ratio:.1f}" if stock.pe_ratio else "N/A"
        
        print(f"{symbol:<12} {name:<25} {price:<12} {change:<12} {market_cap:<15} {pe_ratio:<8}")

def display_detailed_stock(ticker):
    """Display detailed information for a specific stock"""
    try:
        stock = Stock.objects.get(ticker=ticker)
        
        print(f"\n{'='*60}")
        print(f"📈 DETAILED STOCK INFORMATION - {stock.ticker}")
        print(f"{'='*60}")
        print(f"Company Name: {stock.name}")
        print(f"Sector: {stock.sector}")
        print(f"Market State: {stock.market_state}")
        print()
        
        print("💰 PRICING INFORMATION")
        print("-"*30)
        print(f"Current Price: ${stock.current_price:.2f}")
        print(f"Previous Close: ${stock.previous_close:.2f}")
        print(f"Price Change: ${stock.price_change:+.2f} ({stock.price_change_percent:+.2f}%)")
        print(f"Day Range: ${stock.day_low:.2f} - ${stock.day_high:.2f}")
        print(f"52W Range: ${stock.fifty_two_week_low:.2f} - ${stock.fifty_two_week_high:.2f}")
        print()
        
        print("📊 MARKET DATA")
        print("-"*30)
        print(f"Market Cap: {stock.market_cap}")
        print(f"Volume: {stock.volume}")
        print(f"Average Volume: {stock.avg_volume}")
        print()
        
        print("📈 FINANCIAL METRICS")
        print("-"*30)
        print(f"P/E Ratio: {stock.pe_ratio:.2f if stock.pe_ratio else 'N/A'}")
        print(f"Beta: {stock.beta:.2f if stock.beta else 'N/A'}")
        print(f"EPS: ${stock.eps:.2f if stock.eps else 'N/A'}")
        dividend_yield_str = f"{(stock.dividend_yield * 100):.2f}%" if stock.dividend_yield else "N/A"
        print(f"Dividend Yield: {dividend_yield_str}")
        print(f"RSI: {stock.rsi:.2f}")
        
    except Stock.DoesNotExist:
        print(f"❌ Stock {ticker} not found in database")

def real_time_price_demo(ticker):
    """Demonstrate real-time price fetching for a specific stock"""
    from stocks.views import get_real_time_price
    from django.test import RequestFactory
    
    print(f"\n🔄 REAL-TIME PRICE DEMO FOR {ticker}")
    print("="*50)
    
    factory = RequestFactory()
    
    for i in range(3):
        print(f"Fetching real-time price... (Attempt {i+1}/3)")
        
        request = factory.get(f'/realtime/{ticker}/')
        response = get_real_time_price(request, ticker)
        
        if response.status_code == 200:
            import json
            data = json.loads(response.content.decode('utf-8'))
            print(f"✅ {data['ticker']}: ${data['current_price']} at {data['timestamp']}")
        else:
            print(f"❌ Error fetching real-time price for {ticker}")
        
        if i < 2:  # Don't wait after the last iteration
            print("Waiting 2 seconds...")
            time.sleep(2)

def main():
    """Main demonstration function"""
    print("🌟 Welcome to the Real-time Stock Data Integration Demo!")
    print("This Django application integrates with Yahoo Finance for live stock data.")
    
    while True:
        print("\n📋 MENU OPTIONS:")
        print("1. 📊 Display Stock Summary")
        print("2. 🔍 View Detailed Stock Info")
        print("3. 🔄 Update All Stock Data")
        print("4. ⚡ Real-time Price Demo")
        print("5. 🚪 Exit")
        
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == '1':
            display_stock_summary()
            
        elif choice == '2':
            ticker = input("Enter stock ticker (e.g., AAPL, TSLA, GOOGL): ").strip().upper()
            display_detailed_stock(ticker)
            
        elif choice == '3':
            print("🔄 Updating all stock data from Yahoo Finance...")
            update_stock_data()
            print("✅ Stock data updated successfully!")
            
        elif choice == '4':
            ticker = input("Enter stock ticker for real-time demo (e.g., AAPL): ").strip().upper()
            real_time_price_demo(ticker)
            
        elif choice == '5':
            print("👋 Thanks for using the Real-time Stock Data Demo!")
            break
            
        else:
            print("❌ Invalid option. Please select 1-5.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()