from django.urls import path
from .views import ModeratorCreateView, GroupModeratorListView, SelfModeratorListView, ModeratorAdminUpdateView, ModeratorSelfUpdateView

app_name = 'moderator'

urlpatterns = [
    path('create/<int:id>/', ModeratorCreateView.as_view(), name='moderator-create'),
    path('list/group/<str:username>/', GroupModeratorListView.as_view(), name='group-moderator-list'),
    path('list/self/', SelfModeratorListView.as_view(), name='self-moderator-list'),
    path('<int:pk>/update/admin/', ModeratorAdminUpdateView.as_view(), name='moderator-update-admin'),
    path('<int:pk>/update/moderator/', ModeratorSelfUpdateView.as_view(), name='moderator-update-moderator'),
]