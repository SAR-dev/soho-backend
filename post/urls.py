from django.urls import path
from post.views.post import GroupPostCreateView, PostRetriveView, GroupPostListView, PostUpdateView, CategoryPostListView, PostVoteView, PostBookmarkView, PostCanVoteView, PostCanCommentView, GroupDiscussionPostCreateView, PostChoiceVoteView, AddAwardView, PostDraftView, PostUpdateRetriveView, DraftPostListView, PostBookmarksView

app_name = 'post'

urlpatterns = [
    path('list/group/<str:username>/type/<str:type>/', GroupPostListView.as_view(), name='group-post-list'),
    path('list/group/<str:username>/category/<str:slug>/', CategoryPostListView.as_view(), name='category-post-list'),
    path('drafts/', DraftPostListView.as_view(), name='drafts-post-list'),
    path('bookmarks/', PostBookmarksView.as_view(), name='bookmarks-post-list'),
    path('create/group/<str:username>/author/', GroupPostCreateView.as_view(), name='group-post-create'),
    path('create/group/<str:username>/subscriber/', GroupDiscussionPostCreateView.as_view(), name='group-discussion-create'),
    path('<int:pk>/', PostRetriveView.as_view(), name='post-retrive'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post-update-delete'),
    path('<int:pk>/updatedata/', PostUpdateRetriveView.as_view(), name='post-update-data'),
    path('<int:pk>/vote/', PostVoteView.as_view(), name='post-votes'),
    path('<int:pk>/choice/vote/<int:id>/', PostChoiceVoteView.as_view(), name='post-choice-vote'),
    path('<int:pk>/bookmark/', PostBookmarkView.as_view(), name='post-bookmark'),
    path('<int:pk>/can_vote/', PostCanVoteView.as_view(), name='post-can-vote'),
    path('<int:pk>/can_comment/', PostCanCommentView.as_view(), name='post-can-comment'),
    path('<int:pk>/draft/', PostDraftView.as_view(), name='post-change-status'),
    path('<int:pk>/award/<int:id>/free/', AddAwardView.as_view(), name='post-awards'),
]
