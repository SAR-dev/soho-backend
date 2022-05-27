from django.urls import path
from .views import AdvertisementRetriveView, AdvertisementUpdateView

app_name = 'advertisement'

urlpatterns = [
    path('<str:username>/', AdvertisementRetriveView.as_view(), name='advertisement-retrive'),
    path('<str:username>/update/', AdvertisementUpdateView.as_view(), name='advertisement-update')
]