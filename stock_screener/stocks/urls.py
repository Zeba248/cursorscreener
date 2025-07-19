from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('', views.home, name='home'),
    path('stocks.json', views.stocks_json, name='stocks_json'),
]