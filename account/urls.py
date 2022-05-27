from django.urls import path
from account.views import UserListView

app_name = 'account'

urlpatterns = [
	path('list/', UserListView.as_view(), name='user-list'),
]