from django.urls import path
from .views import ImageCreateView, ImageRetriveView, ImageUpdateView

app_name = 'image'

urlpatterns = [
    path('create/', ImageCreateView.as_view(), name='image-create'),
    path('<int:pk>/', ImageRetriveView.as_view(), name='image-retrive'),
    path('<int:pk>/update/', ImageUpdateView.as_view(), name='image-update')
]