from django.urls import path
from .views import PaymentProductView, PaymentCouponView, PaymentPriceView, PaymentCheckoutView, PaymentWebhookView, PaymentPromotionView

app_name = 'payment'

urlpatterns = [
    path('products/', PaymentProductView.as_view(), name='product'),
    path('price/', PaymentPriceView.as_view(), name='price'),
    path('coupons/', PaymentCouponView.as_view(), name='coupon'),
    path('promotions/', PaymentPromotionView.as_view(), name='promotions'),
    path('checkout/', PaymentCheckoutView.as_view(), name='checkout'),
    path('webhook/', PaymentWebhookView.as_view(), name='webhook'),
]