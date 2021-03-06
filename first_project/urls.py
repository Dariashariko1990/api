"""first_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

from orders.views import OrdersView, ContactView, PhoneView
from shop.views import CategoryView, ShopView, ProductView, CartView
from orders.views import PhoneViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders/phone', PhoneViewSet, basename='phone')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('shops/', ShopView.as_view(), name='shops'),
    path('products/', ProductView.as_view(), name='products'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('cart/', CartView.as_view(), name='cart'),
    path('address/', ContactView.as_view(), name='address'),
    #path('phone/', PhoneView.as_view(), name='phone'),
    path('users/', include('users.urls')),
    path('partners/', include('partners.urls')),
]
