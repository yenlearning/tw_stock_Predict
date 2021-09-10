from django.urls import path
from . import views
 
urlpatterns = [
    path('stock_linebot', views.callback)
]