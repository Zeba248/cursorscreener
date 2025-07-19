from django.core.management.base import BaseCommand
from stocks.models import Stock
import yfinance as yf


class Command(BaseCommand):
    help = 'Update stock data from Yahoo Finance'

    def handle(self, *args, **options):
        tickers = ['TSLA', 'AAPL', 'INFY.NS', 'RELIANCE.NS', 'TCS.NS']
        
        self.stdout.write('Updating stock data...')
        
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
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Updated {symbol}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error updating {symbol}: {e}')
                )
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
        
        self.stdout.write(
            self.style.SUCCESS('✅ Stock data update completed!')
        )