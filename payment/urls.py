from django.urls import path
from .views import PayorPaymentView, PayeePaymentView, PaymentProductView, PaymentCouponView, PaymentPriceView, PaymentCheckoutView, PaymentWebhookView

app_name = 'payment'

urlpatterns = [
    path('products/', PaymentProductView.as_view(), name='product'),
    path('prices/', PaymentPriceView.as_view(), name='price'),
    path('coupons/', PaymentCouponView.as_view(), name='coupon'),
    path('checkout/', PaymentCheckoutView.as_view(), name='checkout'),
    path('webhook/', PaymentWebhookView.as_view(), name='webhook'),
    path('payor/', PayorPaymentView.as_view(), name='payor'),
    path('payee/', PayeePaymentView.as_view(), name='payee')
]