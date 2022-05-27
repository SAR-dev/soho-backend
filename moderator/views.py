from rest_framework.views import APIView
from .models import Moderator
from group.models import Group
from .serializers import ModeratorListSerializer, ModeratorCreateSerializer, ModeratorRetriveSerializer, ModeratorAdminUpdateSerializer, ModeratorSelfUpdateSerializer
from utils.paginations import PazeSizePagination
from rest_framework import generics, views, response, permissions, serializers
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django_filters import rest_framework as filters
from django_filters import MultipleChoiceFilter
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()

class IsGroupAuthor(permissions.BasePermission):
    message = 'You can not view this route!'

    def has_permission(self, request, view):
        try:
            obj = Moderator.objects.get(pk=view.kwargs.get('pk'))
            admin = request.user == obj.admin
            return admin
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
        
class IsModerator(permissions.BasePermission):
    message = 'You can not view this route!'

    def has_permission(self, request, view):
        try:
            obj = Moderator.objects.get(pk=view.kwargs.get('pk'))
            moderator = request.user == obj.moderator
            return moderator
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

class IsGroupAuthorAndNotModerator(permissions.BasePermission):
    message = 'You can not view this route!'

    def has_permission(self, request, view):
        try:
            group = Group.objects.get(author=request.user)
            moderator = Moderator.objects.filter(admin=request.user, moderator__id=view.kwargs.get('id')).exists()
            author = group.author == request.user
            return author and not moderator
            
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
        
class ModeratorFilter(filters.FilterSet):
    o = filters.OrderingFilter(
        fields=(
            ('is_verified', 'is_verified'),
        ),
    )
    
    class Meta:
        model = Moderator
        fields = ['is_verified']
        
class ModeratorCreateView(generics.CreateAPIView):
    def perform_create(self, serializer):
        serializer.save(admin=self.request.user, moderator=User.objects.get(id=self.kwargs['id']))

    permission_classes = [IsGroupAuthorAndNotModerator]
    queryset = Moderator.objects.all()
    serializer_class = ModeratorCreateSerializer
    
class GroupModeratorListView(generics.ListAPIView):
    # permission_classes = [IsGroupSubscriber]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ModeratorListSerializer
    pagination_class = PazeSizePagination
    filterset_class = ModeratorFilter

    def get_queryset(self):
        return Moderator.objects.select_related('admin').filter(admin__username=self.kwargs['username'])
    
class SelfModeratorListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ModeratorListSerializer
    pagination_class = PazeSizePagination
    filterset_class = ModeratorFilter

    def get_queryset(self):
        return Moderator.objects.select_related('moderator').filter(moderator=self.request.user)
    
class ModeratorAdminUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsGroupAuthor]
    queryset = Moderator.objects.all()
    serializer_class = ModeratorAdminUpdateSerializer
    
class ModeratorSelfUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsModerator]
    queryset = Moderator.objects.all()
    serializer_class = ModeratorSelfUpdateSerializer