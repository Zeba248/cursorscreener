from django.db import models
from django.utils import timezone

class Stock(models.Model):
    ticker = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, default="N/A")
    
    # Price information
    current_price = models.FloatField(default=0.0)
    previous_close = models.FloatField(default=0.0)
    price_change = models.FloatField(default=0.0)
    price_change_percent = models.FloatField(default=0.0)
    
    # Market data
    market_cap = models.CharField(max_length=20, default="N/A")
    volume = models.CharField(max_length=20, default="N/A")
    avg_volume = models.CharField(max_length=20, default="N/A")
    
    # Trading range
    day_high = models.FloatField(default=0.0)
    day_low = models.FloatField(default=0.0)
    fifty_two_week_high = models.FloatField(default=0.0)
    fifty_two_week_low = models.FloatField(default=0.0)
    
    # Financial metrics
    pe_ratio = models.FloatField(null=True, blank=True)
    dividend_yield = models.FloatField(null=True, blank=True)
    beta = models.FloatField(null=True, blank=True)
    eps = models.FloatField(null=True, blank=True)
    
    # Technical indicators
    rsi = models.FloatField(default=50.0)
    
    # Status fields
    is_positive = models.BooleanField(default=False)
    market_state = models.CharField(max_length=20, default="REGULAR")
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.ticker} - {self.name}"
    
    class Meta:
        ordering = ['-price_change_percent']
