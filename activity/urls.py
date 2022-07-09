from django.urls import path
from activity.views import ActivityListView, ActivityNotificationsListView, MarkAllNotificationsAsRead, MarkSingleNotificationAsRead

app_name = 'activity'

urlpatterns = [
    path('list/<str:username>/', ActivityListView.as_view(), name='acivity-list'),
    path('notifications/', ActivityNotificationsListView.as_view(), name='notifications'),
    path('notifications/done/', MarkAllNotificationsAsRead.as_view(), name='notifications-mark-read'),
    path('notifications/<int:pk>/done/', MarkSingleNotificationAsRead.as_view(), name='notifications-single-read'),
]
