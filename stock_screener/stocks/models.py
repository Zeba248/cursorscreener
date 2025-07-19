from django.db import models
from django.utils import timezone

class Stock(models.Model):
    ticker = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, default="N/A")
    price_change = models.FloatField()
    rsi = models.FloatField(default=50.0)
    volume = models.CharField(max_length=20, default="N/A")
    market_cap = models.CharField(max_length=20, default="N/A")
    is_positive = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.ticker} - {self.name}"
    
    class Meta:
        ordering = ['-price_change']
