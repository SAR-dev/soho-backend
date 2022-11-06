from django.urls import path
from .views import PaymentProductView, PaymentCouponView, PaymentPriceView, PaymentCheckoutView, PaymentWebhookView

app_name = 'payment'

urlpatterns = [
    path('products/', PaymentProductView.as_view(), name='product'),
    path('prices/', PaymentPriceView.as_view(), name='price'),
    path('coupons/', PaymentCouponView.as_view(), name='coupon'),
    path('checkout/', PaymentCheckoutView.as_view(), name='checkout'),
    path('webhook/', PaymentWebhookView.as_view(), name='webhook'),
]