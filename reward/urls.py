from django.urls import path
from .views import RewardPointsView

app_name = 'reward'

urlpatterns = [
    path('points/', RewardPointsView.as_view(), name='reward-points-view'),
]