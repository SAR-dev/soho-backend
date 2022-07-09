from django.shortcuts import render
from utils.paginations import PazeSizePagination
from rest_framework import generics, views, response, permissions, serializers
from rest_framework import filters as rest_framework_filters
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from account.serializers.account import UserListSerializer, UserUpdateSerializer
User = get_user_model()

class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    pagination_class = PazeSizePagination
    filter_backends = [rest_framework_filters.SearchFilter]
    search_fields = ['email', 'first_name', 'last_name', 'username']

class MeRetriveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserUpdateSerializer
    
    def get_object(self):
        try:
            return User.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)