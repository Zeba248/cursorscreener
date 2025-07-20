# 🚀 Real-time Stock Data Integration with YFinance

This Django project provides comprehensive real-time stock market data integration using Yahoo Finance API through the `yfinance` library. The system fetches and displays live stock data without any modifications to the original data format from Yahoo Finance.

## ✨ Features

### 📊 Comprehensive Stock Data
- **Real-time Price Information**: Current price, previous close, price changes
- **Trading Data**: Volume, average volume, day range, 52-week range
- **Financial Metrics**: P/E ratio, Beta, EPS, dividend yield
- **Market Information**: Market cap, sector, market state
- **Technical Indicators**: RSI (customizable for additional indicators)

### ⚡ Real-time Updates
- **Auto-refresh**: Data updates every 5 minutes automatically
- **Manual Refresh**: On-demand data updates
- **Live API Endpoints**: Real-time price fetching for individual stocks
- **Background Updates**: Scheduled data updates via management commands

### 🌐 Multi-Market Support
- **US Markets**: NASDAQ, NYSE (AAPL, GOOGL, MSFT, TSLA, etc.)
- **Indian Markets**: NSE stocks (RELIANCE.NS, TCS.NS, INFY.NS, etc.)
- **Extensible**: Easy to add more markets and stock symbols

## 🛠️ Technical Implementation

### Models
The `Stock` model includes comprehensive fields for real-time data:

```python
class Stock(models.Model):
    # Basic Info
    ticker = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, default="N/A")
    
    # Price Information
    current_price = models.FloatField(default=0.0)
    previous_close = models.FloatField(default=0.0)
    price_change = models.FloatField(default=0.0)
    price_change_percent = models.FloatField(default=0.0)
    
    # Market Data
    market_cap = models.CharField(max_length=20, default="N/A")
    volume = models.CharField(max_length=20, default="N/A")
    avg_volume = models.CharField(max_length=20, default="N/A")
    
    # Trading Range
    day_high = models.FloatField(default=0.0)
    day_low = models.FloatField(default=0.0)
    fifty_two_week_high = models.FloatField(default=0.0)
    fifty_two_week_low = models.FloatField(default=0.0)
    
    # Financial Metrics
    pe_ratio = models.FloatField(null=True, blank=True)
    dividend_yield = models.FloatField(null=True, blank=True)
    beta = models.FloatField(null=True, blank=True)
    eps = models.FloatField(null=True, blank=True)
```

### API Endpoints

#### 1. Stock Data API
```
GET /stocks.json
```
Returns comprehensive data for all tracked stocks:
```json
{
  "last_updated": "2025-01-20 10:30:00",
  "total_stocks": 15,
  "stocks": [
    {
      "ticker": "AAPL",
      "name": "Apple Inc.",
      "sector": "Technology",
      "current_price": 211.18,
      "previous_close": 210.01,
      "price_change": 1.17,
      "price_change_percent": 0.55,
      "market_cap": "$3.21T",
      "volume": "45.2M",
      "day_high": 212.50,
      "day_low": 209.80,
      "pe_ratio": 28.5,
      "beta": 1.2,
      "market_state": "REGULAR"
    }
  ]
}
```

#### 2. Real-time Price API
```
GET /realtime/<ticker>/
```
Returns real-time price for a specific stock:
```json
{
  "ticker": "AAPL",
  "current_price": 211.25,
  "timestamp": "2025-01-20 10:35:00"
}
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Django 5.2.4
- Virtual environment (recommended)

### Installation

1. **Clone and Setup**
```bash
cd stock_screener
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Initial Data Load**
```bash
python manage.py update_stocks
```

4. **Run Development Server**
```bash
python manage.py runserver 0.0.0.0:8000
```

### 🎯 Usage Examples

#### Web Interface
Visit `http://localhost:8000` to see the beautiful real-time stock dashboard with:
- Live updating stock cards
- Comprehensive financial metrics
- Auto-refresh functionality
- Responsive design

#### Command Line Interface
Run the interactive demo:
```bash
source venv/bin/activate
python demo_realtime.py
```

#### Management Commands
Update stock data manually:
```bash
python manage.py update_stocks
```

#### API Usage
```python
import requests

# Get all stocks data
response = requests.get('http://localhost:8000/stocks.json')
data = response.json()
print(f"Total stocks: {data['total_stocks']}")

# Get real-time price for AAPL
response = requests.get('http://localhost:8000/realtime/AAPL/')
price_data = response.json()
print(f"AAPL current price: ${price_data['current_price']}")
```

## 📈 Data Sources and Accuracy

### Yahoo Finance Integration
- **Source**: Yahoo Finance API via `yfinance` library
- **Update Frequency**: Real-time (with 15-minute delay for some markets)
- **Data Integrity**: No modifications to original Yahoo Finance data
- **Reliability**: Production-ready with error handling and fallbacks

### Supported Stock Symbols
Current implementation includes:
- **US Tech**: AAPL, GOOGL, MSFT, TSLA, AMZN, NVDA, META, NFLX, AMD, INTC
- **Indian Stocks**: RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, ICICIBANK.NS

### Adding New Stocks
Modify the `tickers` list in `stocks/views.py` or `stocks/management/commands/update_stocks.py`:

```python
tickers = [
    'AAPL', 'GOOGL', 'MSFT',  # US stocks
    'RELIANCE.NS', 'TCS.NS',  # Indian stocks
    'YOUR_STOCK_HERE'         # Add new stocks
]
```

## 🔧 Configuration

### Auto-refresh Settings
In `templates/stocks/index.html`, modify the refresh interval:
```javascript
// Refresh every 5 minutes (300,000 milliseconds)
refreshInterval = setInterval(loadStockData, 300000);
```

### Stock Data Update Frequency
In `stocks/views.py`, modify the update threshold:
```python
# Check if data needs updating (every 5 minutes for real-time feel)
needs_update = not stocks or (stocks and stocks[0].last_updated < timezone.now() - timedelta(minutes=5))
```

## 🎨 Frontend Features

### Modern UI/UX
- **Gradient Design**: Beautiful color schemes and animations
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Live data without page refresh
- **Interactive Cards**: Hover effects and smooth transitions
- **Status Indicators**: Visual indicators for market state and price changes

### Technical Stack
- **Frontend**: Bootstrap 5.3, Custom CSS, Vanilla JavaScript
- **Backend**: Django 5.2.4, Python 3.8+
- **Database**: SQLite (easily configurable to PostgreSQL/MySQL)
- **API**: RESTful JSON endpoints

## 🔒 Error Handling

### Robust Error Management
- **API Failures**: Graceful fallbacks when Yahoo Finance is unavailable
- **Data Validation**: Comprehensive validation of incoming stock data
- **Network Issues**: Retry mechanisms and timeout handling
- **User Experience**: Clear error messages and loading states

### Logging and Monitoring
The system includes comprehensive logging:
```python
import logging
logger = logging.getLogger(__name__)

try:
    # Stock data fetching
    stock = yf.Ticker(symbol)
    info = stock.info
    # ... processing
except Exception as e:
    logger.error(f"Error fetching data for {symbol}: {e}")
    # Fallback handling
```

## 📊 Performance Optimization

### Efficient Data Handling
- **Batch Updates**: All stocks updated in single database transaction
- **Caching Strategy**: Intelligent caching to reduce API calls
- **Lazy Loading**: On-demand data fetching for individual stocks
- **Database Indexing**: Optimized queries for fast data retrieval

### Scalability Considerations
- **Database**: Easily scalable to PostgreSQL for production
- **Caching**: Redis integration ready for high-traffic scenarios
- **API Rate Limits**: Built-in handling of Yahoo Finance rate limits
- **Background Jobs**: Celery-ready for asynchronous processing

## 🚀 Deployment

### Production Readiness
The application is designed for production deployment with:
- **Environment Variables**: Secure configuration management
- **Static Files**: Proper static file handling
- **Database**: Production database support
- **Security**: CSRF protection, secure headers

### Docker Support (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contributing

### Adding New Features
1. **New Stock Markets**: Extend ticker list and format handling
2. **Technical Indicators**: Add RSI, MACD, moving averages
3. **Alerts**: Price alerts and notifications
4. **Historical Data**: Charts and trend analysis
5. **Portfolio Tracking**: User portfolios and watchlists

### Code Structure
- `stocks/models.py`: Database models
- `stocks/views.py`: API endpoints and business logic
- `stocks/management/commands/`: Management commands
- `templates/stocks/`: Frontend templates
- `static/`: CSS, JavaScript, images

## 📞 Support

For questions, issues, or feature requests:
1. Check the Django logs for detailed error information
2. Verify Yahoo Finance API availability
3. Ensure proper virtual environment activation
4. Review database migrations status

## 📄 License

This project demonstrates real-time stock data integration for educational and development purposes. Please ensure compliance with Yahoo Finance Terms of Service when using in production.

---

**Happy Trading! 📈✨**

*Built with ❤️ using Django and Yahoo Finance API*