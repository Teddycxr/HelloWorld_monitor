"""HelloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path
from django.conf.urls import url
from django.urls import path
from . import views
# from . import events

urlpatterns = [
    url('^$', views.portal),
    path('usdtSwap/<str:symbol>/', views.usdtSwap),
    path('coins/<str:symbol>/', views.coins), #1
    path('coinSwap/<str:symbol>/', views.coinSwap),
    path('combo/<str:symbol>/', views.combo),
    path('spot/<str:symbol>/', views.spot),
    path('binanceUsdtSwap/<str:symbol>/', views.binanceUsdtSwap),
    path('arbitrage/<str:symbol>/', views.arbitrage),
    path('coinStore/<str:symbol>/', views.coinStore), #1
    path('coinStoredepth/<str:symbol>/', views.coinStoredepth), #1
    path('coinStoreUsdtSwap/<str:symbol>/', views.coinStoreUsdtSwap), #1
    path('etp/<str:symbol>/', views.etp),
    path('hedgeAccount/', views.hedgeAccount),
    path('depth/<str:symbol>/', views.depth), #
    path('fundingRate/', views.fundingRate),
    path('<str:kind>/<str:symbol>/openOrders/', views.openOrders),
    path('<str:kind>/<str:symbol>/<str:strategy>/hisDeals/', views.hisDeals),
    #path('coinTRUsdtSwap/<str:symbol>', views.coinTRUsdtSwap),
    #path('cointrSpot/<str:symbol>', views.cointrSpot),
    # path('test/', events.test),
    # path('usdtSwap/btcusdt/', views.btcusdt),
    # path('usdtSwap/ethusdt/', views.ethusdt),
    # path('usdtSwap/eosusdt/', views.eosusdt),
    # path('coins/', views.btcusdt),
    # path('coinSwap/', views.btcusdt),
]
