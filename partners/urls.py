from django.urls import path
from partners import views

app_name = 'partners'

urlpatterns = [
    path('update/', views.PartnerUpdate.as_view(), name='partner-update'),
    path('state/', views.PartnerState.as_view(), name='partner-state'),
    path('orders/', views.PartnerOrders.as_view(), name='partner-orders'),
]
