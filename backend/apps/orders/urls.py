from django.urls import path
from .views import CheckoutAPIView, MpesaCallbackAPIView, OrderStatusAPIView

urlpatterns = [
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('payments/mpesa/callback/', MpesaCallbackAPIView.as_view(), name='mpesa-callback'),
    path('<uuid:order_id>/status/', OrderStatusAPIView.as_view(), name='order-status'),
]
