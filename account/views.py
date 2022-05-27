from django.shortcuts import render
from utils.paginations import PazeSizePagination
from rest_framework import generics, views, response, permissions, serializers
from rest_framework import filters as rest_framework_filters
from django.contrib.auth import get_user_model
User = get_user_model()
from account.serializers.account import UserListSerializer
        
class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    pagination_class = PazeSizePagination
    filter_backends = [rest_framework_filters.SearchFilter]
    search_fields = ['email', 'first_name', 'last_name', 'username']