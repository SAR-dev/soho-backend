from django.urls import path
from .views.group import GroupListView, GroupRulesUpdateView, GroupPaymentRetriveView, GroupSubscribedListView, GroupRetriveView, GroupRulesRetriveView, GroupUpdateView, GroupSubscribersView, GroupBlacklistSubscriberView,GroupSubscribeView, GroupBlacklistView, GroupLeaderboardView
from .views.category import GroupCategoryListView, GroupCategoryCreateView, GroupCategoryRetriveView, GroupCategoryUpdateView
from .views.subcategory import GroupSubCategoryCreateView, ChangeParentCategoryView, UpdateSubCategoryView

app_name = 'group'

urlpatterns = [
    path('', GroupListView.as_view(), name='group-list'),
    path('subscribed/', GroupSubscribedListView.as_view(), name='group-subscribed-list'),
    path('<str:username>/', GroupRetriveView.as_view(), name='group-retrive'),
    path('<str:username>/rules/', GroupRulesRetriveView.as_view(), name='group-rules-retrive'),
    path('<str:username>/payment/', GroupPaymentRetriveView.as_view(), name='group-payment-retrive'),
    path('<str:username>/rules/update/', GroupRulesUpdateView.as_view(), name='group-rules-update'),
    path('<str:username>/update/', GroupUpdateView.as_view(), name='group-update'),
    # path('<str:username>/subscribe/<str:token>/', GroupSubscribeView.as_view(), name='group-subscribe'),
    path('<str:username>/subscribe/', GroupSubscribeView.as_view(), name='group-subscribe'),
    path('<str:username>/blacklist/<int:user_id>/', GroupBlacklistSubscriberView.as_view(), name='group-blacklist-subscriber'),
    path('<str:username>/subscribers/', GroupSubscribersView.as_view(), name='group-subscribers'),
    path('<str:username>/blacklists/', GroupBlacklistView.as_view(), name='group-blacklists'),
    path('<str:username>/leaderboard/<str:timespan>/', GroupLeaderboardView.as_view(), name='group-leaderboard'),
    path('<str:username>/categories/', GroupCategoryListView.as_view(), name='group-categories'),
    path('<str:username>/categories/create/', GroupCategoryCreateView.as_view(), name='group-categories-create'),
    path('<str:username>/categories/<str:slug>/', GroupCategoryRetriveView.as_view(), name='group-categories-retrive'),
    path('<str:username>/subcategory/<str:slug>/relocate/', ChangeParentCategoryView.as_view(), name='group-subcategory-relocate'),
    path('<str:username>/subcategory/<str:slug>/update/', UpdateSubCategoryView.as_view(), name='group-subcategory-update'),
    path('<str:username>/categories/<str:slug>/update/', GroupCategoryUpdateView.as_view(), name='group-categories-update'),
    path('<str:username>/categories/<str:slug>/subcategory/create/', GroupSubCategoryCreateView.as_view(), name='group-sub-categoriy-create'),
]