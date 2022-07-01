from rest_framework.views import APIView
from post.models import Post
from moderator.models import Moderator
from activity.models import Activity
from group.models import Group, Category
from choice.models import Choice
from reward.models import Reward
from award.models import Award
from post.serializers.post import PostCreateSerializer, PostReriveSerializer, PostListSerializer, PostUpdateSerializer, DiscussionPostCreateSerializer, PostBookmarksSerializer
from utils.paginations import PazeSizePagination
from utils.get_seconds import get_seconds
from rest_framework import generics, views, response, permissions, serializers
from rest_framework.exceptions import NotFound, PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django_filters import rest_framework as filters
from django_filters import MultipleChoiceFilter
from django.db.models import Q
from django.utils import timezone


class IsGroupAuthor(permissions.BasePermission):
    message = 'You can not view this route!'

    def has_permission(self, request, view):
        try:
            group = Group.objects.select_related('author').get(
                author__username=view.kwargs.get('username')
            )
            author = group.author == request.user
            return author
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class IsGroupAuthorOrModerator(permissions.BasePermission):
    message = 'You can not view this route!'

    def has_permission(self, request, view):
        try:
            group = Group.objects.select_related('author').get(
                author__username=view.kwargs.get('username')
            )
            author = group.author == request.user
            moderator = Moderator.verified.filter(
                moderator=request.user, admin=group.author).exists()
            return author or moderator
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class IsGroupSubscriber(permissions.BasePermission):
    message = 'You need to be a subscriber.'

    def has_permission(self, request, view):
        try:
            group = Group.objects.select_related('author').get(
                author__username=view.kwargs.get('username')
            )
            subscriber = group.subscribers.filter(pk=request.user.id).exists()
            return subscriber
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class IsPostGroupSubscriber(permissions.BasePermission):
    message = 'You can not view this route!'

    def has_permission(self, request, view):
        try:
            post = Post.objects.get(pk=view.kwargs.get('pk'))
            subscriber = post.group.subscribers.filter(
                pk=request.user.id).exists()
            return subscriber
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class IsValidChoiceGroupSubscriber(permissions.BasePermission):
    message = 'You can not view this route!'

    def has_permission(self, request, view):
        try:
            post = Post.published.get(pk=view.kwargs.get('pk'))
            subscriber = post.group.subscribers.filter(
                pk=request.user.id).exists()
            valid = False
            for choice in post.choices.all():
                if choice.id == view.kwargs.get('id'):
                    valid = True
            return subscriber and valid
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class IsCategoryGroupSubscriber(permissions.BasePermission):
    message = 'You can not view this route!'

    def has_permission(self, request, view):
        try:
            category = Category.objects.get(slug=view.kwargs.get('slug'))
            subscriber = category.group.subscribers.filter(
                pk=request.user.id).exists()
            return subscriber
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class IsPostAuthor(permissions.BasePermission):
    message = 'Only author can view this!'

    def has_permission(self, request, view):
        try:
            post = Post.objects.get(pk=view.kwargs.get('pk'))
            author = post.author == request.user
            return author
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class IsPostGroupAndAwardSubscriber(permissions.BasePermission):
    message = 'You can not view this route!'

    def has_permission(self, request, view):
        try:
            post = Post.published.get(pk=view.kwargs.get('pk'))
            subscriber = post.group.subscribers.filter(
                pk=request.user.id).exists()
            award = Award.free.get(pk=view.kwargs.get('id'))
            return subscriber and (award.author.id == post.group.author.id or award.public == True)
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class PostFilter(filters.FilterSet):
    o = filters.OrderingFilter(
        fields=(
            ('content', 'content'),
            ('created_at', 'created_at'),
        ),
    )

    class Meta:
        model = Post
        post_type = MultipleChoiceFilter(conjoined=True)
        fields = {
            'content': ['icontains'],
            'author__username': ['icontains'],
            'author__first_name': ['icontains'],
            'author__last_name': ['icontains'],
        }


class GroupPostListView(generics.ListAPIView):
    # permission_classes = [IsGroupSubscriber]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostListSerializer
    pagination_class = PazeSizePagination
    filterset_class = PostFilter

    def get_queryset(self):
        if self.kwargs["type"] == "all":
            return Post.published.select_related('group').filter(group__author__username=self.kwargs["username"])
        elif self.kwargs["type"] == "discussion":
            return Post.published.select_related('group').filter(group__author__username=self.kwargs["username"], post_type="discussion")
        elif self.kwargs["type"] == "poll":
            return Post.published.select_related('group').filter(group__author__username=self.kwargs["username"], post_type="poll")
        elif self.kwargs["type"] == "ama":
            return Post.published.select_related('group').filter(group__author__username=self.kwargs["username"], post_type="ama")
        elif self.kwargs["type"] == "announcement":
            return Post.published.select_related('group').filter(group__author__username=self.kwargs["username"], post_type="announcement")
        elif self.kwargs["type"] == "premier":
            return Post.published.select_related('group').filter(group__author__username=self.kwargs["username"], post_type="premier")
        elif self.kwargs["type"] == "drop":
            return Post.published.select_related('group').filter(group__author__username=self.kwargs["username"], post_type="drop")
        else:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class CategoryPostListView(generics.ListAPIView):
    # permission_classes = [IsCategoryGroupSubscriber]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostListSerializer
    pagination_class = PazeSizePagination
    filterset_class = PostFilter

    def get_queryset(self):
        return Post.published.select_related('group').filter(group__author__username=self.kwargs["username"], category__slug=self.kwargs["slug"])

class SubCategoryPostListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostListSerializer
    pagination_class = PazeSizePagination
    filterset_class = PostFilter

    def get_queryset(self):
        return Post.published.select_related('group').filter(group__author__username=self.kwargs["username"], sub_category__slug=self.kwargs["slug"])
    
class PostListView(generics.ListAPIView):
    # permission_classes = [IsGroupSubscriber]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostListSerializer
    pagination_class = PazeSizePagination
    filterset_class = PostFilter

    def get_queryset(self):
        return Post.published.select_related('group').filter(group__author__username=self.kwargs["username"])


class PostBookmarksView(generics.ListAPIView):
    # permission_classes = [IsGroupSubscriber]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostBookmarksSerializer
    pagination_class = PazeSizePagination
    filterset_class = PostFilter

    def get_queryset(self):
        return Post.published.filter(bookmarks__id=self.request.user.id)


class DraftPostListView(generics.ListAPIView):
    # permission_classes = [IsGroupSubscriber]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostListSerializer
    pagination_class = PazeSizePagination
    filterset_class = PostFilter

    def get_queryset(self):
        return Post.draft.filter(author__id=self.request.user.id)


class GroupDiscussionPostCreateView(generics.CreateAPIView):
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, group=Group.objects.select_related('author').get(
            author__username=self.kwargs['username']
        ))

    permission_classes = [IsGroupSubscriber]
    queryset = Post.objects.all()
    serializer_class = DiscussionPostCreateSerializer


class GroupPostCreateView(generics.CreateAPIView):
    def perform_create(self, serializer):
        if 'category' in self.request.data:
            category = self.request.data['category']
        else:
            category = False
        if category:
            categories = Category.objects.select_related('group').filter(
                group__author__username=self.kwargs["username"])
            if(categories.filter(id=self.request.data['category']).exists()):
                serializer.save(author=self.request.user, group=Group.objects.select_related('author').get(
                    author__username=self.kwargs['username']
                ))
            else:
                raise NotFound(
                    detail="Error 404, Selected category not found!", code=404)
        else:
            serializer.save(author=self.request.user, group=Group.objects.select_related('author').get(
                author__username=self.kwargs['username']
            ))

    permission_classes = [IsGroupAuthorOrModerator]
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class PostRetriveView(generics.RetrieveAPIView):
    # permission_classes = [IsPostGroupSubscriber]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.published.all()
    serializer_class = PostReriveSerializer


class PostUpdateRetriveView(generics.RetrieveAPIView):
    permission_classes = [IsPostAuthor]
    queryset = Post.objects.all()
    serializer_class = PostReriveSerializer


class PostUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsPostAuthor]
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer


class PostVoteView(views.APIView):
    permission_classes = [IsPostGroupSubscriber]

    def get(self, request, pk):
        try:
            post = Post.published.get(pk=pk)
            auth_user = self.request.user
            return response.Response({
                'count': post.votes.count_up(),
                'upvoted': post.votes.exists_up(auth_user.id),
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def post(self, request, pk):
        try:
            post = Post.canvote.get(pk=pk)
            auth_user = self.request.user
            post.votes.up(auth_user.id)
            # post clapped
            Activity.objects.create(target=post.id, group_id=post.group.id,
                                    sender_id=request.user.id, reciever_id=post.author.id, target_type="post", verb="clapped")
            return response.Response({
                'count': post.votes.count_up(),
                'upvoted': True,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def delete(self, request, pk):
        try:
            post = Post.canvote.get(pk=pk)
            auth_user = self.request.user
            post.votes.delete(auth_user.id)
            # post unclapped
            Activity.objects.filter(target=post.id, group_id=post.group.id,
                                    sender_id=request.user.id, reciever_id=post.author.id, target_type="post", verb="clapped").delete()
            return response.Response({
                'count': post.votes.count_up(),
                'upvoted': False,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class PostBookmarkView(views.APIView):
    permission_classes = [IsPostGroupSubscriber]

    def get(self, request, pk):
        try:
            post = Post.canbookmark.get(pk=pk)
            bookmarked = request.user in post.bookmarks.all()
            count = post.bookmarks.count()
            return response.Response({
                'bookmarked': bookmarked,
                'count': count,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def post(self, request, pk):
        try:
            post = Post.canbookmark.get(pk=pk)
            if request.user not in post.bookmarks.all():
                post.bookmarks.add(request.user)

            count = post.bookmarks.count()
            return response.Response({
                'bookmarked': True,
                'count': count,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def delete(self, request, pk):
        try:
            post = Post.canbookmark.get(pk=pk)
            if request.user in post.bookmarks.all():
                post.bookmarks.remove(request.user)

            count = post.bookmarks.count()
            return response.Response({
                'bookmarked': False,
                'count': count,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class PostCanVoteView(views.APIView):
    permission_classes = [IsPostAuthor]

    def get(self, request, pk):
        try:
            post = Post.published.get(pk=pk)
            can_vote = post.can_vote
            return response.Response({
                'can_vote': can_vote,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def post(self, request, pk):
        try:
            post = Post.published.get(pk=pk)
            post.can_vote = True
            post.save()
            return response.Response({
                'can_vote': True,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def delete(self, request, pk):
        try:
            post = Post.published.get(pk=pk)
            post.can_vote = False
            post.save()
            return response.Response({
                'can_vote': False,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class PostCanCommentView(views.APIView):
    permission_classes = [IsPostAuthor]

    def get(self, request, pk):
        try:
            post = Post.published.get(pk=pk)
            can_comment = post.can_comment
            return response.Response({
                'can_comment': can_comment,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def post(self, request, pk):
        try:
            post = Post.published.get(pk=pk)
            post.can_comment = True
            post.save()
            return response.Response({
                'can_comment': True,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def delete(self, request, pk):
        try:
            post = Post.published.get(pk=pk)
            print(post)
            post.can_comment = False
            post.save()
            return response.Response({
                'can_comment': False,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class PostDraftView(views.APIView):
    permission_classes = [IsPostAuthor]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            status = post.status
            return response.Response({
                'status': status,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.status = "draft"
            post.save()
            return response.Response({
                'status': "draft",
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.status = "published"
            post.save()
            return response.Response({
                'status': "published",
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class PostChoiceVoteView(views.APIView):
    permission_classes = [IsValidChoiceGroupSubscriber]

    def get(self, request, pk, id):
        try:
            auth_user = self.request.user
            choice = Choice.objects.get(pk=id)
            return response.Response({
                'count': choice.votes.count_up(),
                'upvoted': choice.votes.exists_up(auth_user.id)
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def post(self, request, pk, id):
        try:
            post = Post.objects.get(pk=pk)
            time_diff = (timezone.localtime() - post.created_at).total_seconds()
            if(time_diff < get_seconds(post.duration)):
                auth_user = self.request.user
                choice = Choice.objects.get(pk=id)
                for item in post.choices.all():
                    if item.id == id:
                        item.votes.up(auth_user.id)
                    else:
                        item.votes.delete(auth_user.id)
                return response.Response({
                    'count': choice.votes.count_up(),
                    'upvoted': True,
                })
            else:
                raise PermissionDenied(detail="Sorry, Time duration expired!")
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def delete(self, request, pk, id):
        try:
            post = Post.objects.get(pk=pk)
            time_diff = (timezone.localtime() - post.created_at).total_seconds()
            if(time_diff < get_seconds(post.duration)):
                auth_user = self.request.user
                choice = Choice.objects.get(pk=id)
                for item in post.choices.all():
                    if item.id == id:
                        item.votes.delete(auth_user.id)
                return response.Response({
                    'count': choice.votes.count_up(),
                    'upvoted': False,
                })
            else:
                raise PermissionDenied(detail="Sorry, Time duration expired!")
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class AddAwardView(views.APIView):
    permission_classes = [IsPostGroupAndAwardSubscriber]

    def get(self, request, pk, id):
        try:
            post = Post.published.get(pk=pk)
            return response.Response(post.awards)
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def post(self, request, pk, id):
        try:
            post = Post.canvote.get(pk=pk)
            auth_user = self.request.user
            if str(id) in post.awards:
                if auth_user.id not in post.awards[str(id)]:
                    post.awards[str(id)].append(auth_user.id)
                    post.save()
            else:
                post.awards[str(id)] = []
                post.awards[str(id)].append(auth_user.id)
                post.save()
            # post awarded
            Activity.objects.create(target=post.id, group_id=post.group.id,
                                    sender_id=request.user.id, reciever_id=post.author.id, target_type="post", verb="awarded")
            return response.Response(post.awards)
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

    def delete(self, request, pk, id):
        try:
            post = Post.canvote.get(pk=pk)
            auth_user = self.request.user
            if str(id) in post.awards:
                if auth_user.id in post.awards[str(id)]:
                    post.awards[str(id)].remove(auth_user.id)
                    post.save()
            else:
                post.awards[str(id)] = []
                post.save()
            # post unawarded
            Activity.objects.filter(target=post.id, group_id=post.group.id,
                                    sender_id=request.user.id, reciever_id=post.author.id, target_type="post", verb="awarded").delete()
            return response.Response(post.awards)
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
