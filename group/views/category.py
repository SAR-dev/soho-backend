from group.models import Group, Category
from utils.paginations import PazeSizePagination
from rest_framework import generics, views, response, permissions, exceptions, status
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from group.serializers.category import GroupCategoryCreateSerializer, GroupCategoryListSerializer, GroupCategoryReriveSerializer, GroupCategoryUpdateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from django_filters import rest_framework as filters


class IsGroupSubscriber(permissions.BasePermission):
    message = 'You need to subscribe to continue!'

    def has_permission(self, request, view):
        try:
            group = Group.objects.select_related('author').get(
                author__username=view.kwargs.get('username')
            )
            return group.subscribers.filter(pk=request.user.id).exists()
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
    
class IsGroupAuthor(permissions.BasePermission):
    message = 'Only author has access!'

    def has_permission(self, request, view):
        try:
            group = Group.objects.select_related('author').get(
                author__username=view.kwargs.get('username')
            )
            return group.author.id == request.user.id
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
        

class CategoryFilter(filters.FilterSet):
    o = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('about', 'about'),
            ('created_at', 'created_at'),
        ),
    )

    class Meta:
        model = Category
        fields = {
            'name': ['icontains'],
            'about': ['icontains'],
        }

class GroupCategoryListView(generics.ListAPIView):
    # permission_classes = [IsGroupSubscriber]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GroupCategoryListSerializer
    pagination_class = PazeSizePagination
    filterset_class = CategoryFilter

    def get_queryset(self):
        try:
            return Category.objects.select_related('group').filter(group__author__username = self.kwargs["username"])
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
       
class GroupCategoryCreateView(generics.CreateAPIView):
    def perform_create(self, serializer):
        serializer.save(group = Group.objects.select_related('author').get(
                author__username=self.kwargs["username"]
            ))

    permission_classes = [IsGroupAuthor]
    queryset = Category.objects.all()
    serializer_class = GroupCategoryCreateSerializer

class GroupCategoryRetriveView(generics.RetrieveAPIView):
    permission_classes = [IsGroupSubscriber]
    serializer_class = GroupCategoryReriveSerializer
    lookup_field = "slug"
    
    def get_queryset(self):
        try:
            return Category.objects.select_related('group').filter(group__author__username = self.kwargs["username"])
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
    
class GroupCategoryUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsGroupAuthor]
    serializer_class = GroupCategoryUpdateSerializer
    lookup_field = "slug"
    
    def get_queryset(self):
        try:
            return Category.objects.select_related('group').filter(group__author__username = self.kwargs["username"])
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
