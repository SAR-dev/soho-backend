from django.urls import path
from .views import CommentCreateView, CommentListView,CommentBanView, CommentChildCreateView, CommentRetriveView, CommentUpdateView, CommentVoteView, CommentHandsRaiseView, CommentPinnedView, CommentPostRetriveView

app_name = 'comment'

urlpatterns = [
    path('create/post/<int:pk>/', CommentCreateView.as_view(), name='comment-create'),
    path('create/post/<int:pk>/parent/<int:parent>/', CommentChildCreateView.as_view(), name='comment-child-create'),
    path('list/post/<int:pk>/', CommentListView.as_view(), name='comment-list'),
    path('<int:pk>/', CommentRetriveView.as_view(), name='comment-retrive'),
    path('<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('<int:pk>/ban/', CommentBanView.as_view(), name='comment-ban'),
    path('<int:pk>/vote/', CommentVoteView.as_view(), name='comment-vote'),
    path('<int:pk>/hands/', CommentHandsRaiseView.as_view(), name='comment-hand-raise'),
    path('<int:pk>/pinned/', CommentPinnedView.as_view(), name='comment-pin'),
    path('<int:pk>/post/', CommentPostRetriveView.as_view(), name='comment-post'),
]