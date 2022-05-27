from django.urls import path
from .views import ProfileListView, ProfileRetrieveView, ProfileUpdateView, ProfileImagesView

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='profile-list'),
    path('update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('images/', ProfileImagesView.as_view(), name='profile-images'),
    path('<str:username>/', ProfileRetrieveView.as_view(), name='profile-retrive'),
]
