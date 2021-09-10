"""final_topic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from myapp.views import login,signup,main,stockPlay
from myapp.views import CheckSignUp
from myapp.views import warehouse_table,buy,income_table
from myapp.views import now_price
from myapp.views import search,logout,main_search
from myapp.views import future_table, future_range_upper, future_range_lower




urlpatterns = [
    #path(網址,函式),
    path('admin/', admin.site.urls),
    path('login/', login),
    path('logout/', logout),
    path('signup/', signup),
    path('CheckSignUp/', CheckSignUp),
    path('main/', main),
    path('stockPlay/', stockPlay),
    path('main/stockPlay.html', stockPlay),
    path('warehouse_table/', warehouse_table),
    path('income_table/', income_table),
    path('buy/', buy),
    path('now_price/',now_price),
    path('search/',search),
    path('main_search/',main_search),
    path('future/',future_table), 
    path('range_upper/',future_range_upper),
    path('range_lower/',future_range_lower),
    path('callback/',include('mylinebot.urls')),

   






]
