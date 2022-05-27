from django.urls import path
from .views import GroupAwardListView, UserAwardListView, AwardCreateView, AwardUpdateView

app_name = 'award'

urlpatterns = [
    path('create/', AwardCreateView.as_view(), name='award-create'),
    path('list/group/<str:username>/', GroupAwardListView.as_view(), name='group-award-list'),
    path('list/user/<str:username>/', UserAwardListView.as_view(), name='user-award-list'),
    path('<int:pk>/update/', AwardUpdateView.as_view(), name='award-update'),
]
