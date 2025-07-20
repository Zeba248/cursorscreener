from django.core.management.base import BaseCommand
from stocks.models import Stock
import yfinance as yf


class Command(BaseCommand):
    help = 'Update stock data from Yahoo Finance with comprehensive real-time information'

    def handle(self, *args, **options):
        # Popular tickers from different markets
        tickers = [
            'AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN',  # US Tech
            'NVDA', 'META', 'NFLX', 'AMD', 'INTC',    # More US Tech
            'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS'  # Indian stocks
        ]
        
        self.stdout.write('Updating comprehensive stock data...')
        
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
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Updated {symbol} - ${current_price:.2f} ({price_change_percent:+.2f}%)')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error updating {symbol}: {e}')
                )
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
        
        self.stdout.write(
            self.style.SUCCESS('✅ Comprehensive stock data update completed!')
        )