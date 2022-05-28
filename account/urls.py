from django.urls import path
from account.views import UserListView, MeRetriveView

app_name = 'account'

urlpatterns = [
	path('list/', UserListView.as_view(), name='user-list'),
	path('me/', MeRetriveView.as_view(), name='me'),
]