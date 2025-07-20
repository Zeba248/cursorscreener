from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('', views.home, name='home'),
    path('stocks.json', views.stocks_json, name='stocks_json'),
    path('realtime/<str:ticker>/', views.get_real_time_price, name='realtime_price'),
]