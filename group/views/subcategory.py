from group.models import Group, Category, SubCategory
from utils.paginations import PazeSizePagination
from rest_framework import generics, views, response, permissions, exceptions, status
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from group.serializers.subcategory import GroupSubCategoryCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from django_filters import rest_framework as filters


class IsGroupAuthor(permissions.BasePermission):
    message = 'Only author has access!'

    def has_permission(self, request, view):
        try:
            category = Category.objects.get(slug=view.kwargs.get('slug'))
            return category.group.author.id == request.user.id
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
        
              
class GroupSubCategoryCreateView(generics.CreateAPIView):
    def perform_create(self, serializer):
        serializer.save(category = Category.objects.get(slug=self.kwargs['slug']))

    permission_classes = [IsGroupAuthor]
    queryset = SubCategory.objects.all()
    serializer_class = GroupSubCategoryCreateSerializer