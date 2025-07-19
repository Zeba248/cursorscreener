from django.contrib import admin
from .models import Stock

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['ticker', 'name', 'sector', 'price_change', 'volume', 'market_cap', 'last_updated']
    list_filter = ['sector', 'is_positive', 'last_updated']
    search_fields = ['ticker', 'name']
    ordering = ['-price_change']
