# Django Stock Screener

This is a Django-based stock screener application converted from Flask. It displays real-time stock information for selected tickers using Yahoo Finance data.

## Features

- Real-time stock data from Yahoo Finance
- Modern Bootstrap UI with responsive design
- Database storage with Django ORM
- Admin interface for managing stocks
- Automatic data refresh
- Management command for updating stock data

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run database migrations:
```bash
python manage.py migrate
```

3. Update stock data:
```bash
python manage.py update_stocks
```

4. (Optional) Create a superuser for admin access:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Open your browser and navigate to `http://127.0.0.1:8000/`

## Usage

### Web Interface
- Visit the main page to view the stock screener
- Data automatically refreshes every 30 minutes
- Click on sorting options to sort by different criteria

### Management Commands
- Update stock data: `python manage.py update_stocks`

### Admin Interface
- Access at `http://127.0.0.1:8000/admin/`
- View and manage stock data
- Filter and search stocks

## API Endpoints

- `/` - Main stock screener page
- `/stocks.json` - JSON API endpoint for stock data

## Stock Tickers

Currently tracking:
- TSLA (Tesla, Inc.)
- AAPL (Apple Inc.)
- INFY.NS (Infosys Limited)
- RELIANCE.NS (Reliance Industries)
- TCS.NS (Tata Consultancy Services)

## Architecture

- **Django Framework**: Web framework and ORM
- **SQLite Database**: Default database for development
- **Yahoo Finance API**: Real-time stock data via `yfinance`
- **Bootstrap 5**: Frontend styling and components
- **JavaScript/AJAX**: Dynamic data loading

## Conversion from Flask

This application was converted from a Flask-based stock screener with the following improvements:

1. **Database Integration**: Uses Django ORM instead of JSON files
2. **Admin Interface**: Built-in Django admin for data management
3. **Management Commands**: Django command system for data updates
4. **Better Structure**: Django's app-based architecture
5. **Automatic Data Refresh**: Smart caching with 30-minute refresh
6. **Error Handling**: Better error handling and logging