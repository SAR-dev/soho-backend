from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics, status, response, views
from .models import Profile
from group.models import Group
from image.models import Image
from .serializers import ProfileListSerializer, ProfileRetriveSerializer, ProfileUpdateSerializer, ProfileImagesSerializer
from utils.paginations import PazeSizePagination
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
User = get_user_model()


class IsOwner(permissions.BasePermission):
    message = 'Only owner can edit his account!'

    def has_permission(self, request, view):
        try:
            obj = Profile.objects.select_related('user').get(
                user__username=view.kwargs.get('username')
            )
            return obj.user.id == request.user.id
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class ProfileFilter(filters.FilterSet):
    o = filters.OrderingFilter(
        fields=(
            ('nickname', 'nickname'),
            ('created_at', 'created_at'),
        ),
    )

    class Meta:
        model = Profile
        fields = {
            'bio': ['icontains'],
            'nickname': ['icontains'],
            'email_address': ['icontains'],
            'phone_number': ['icontains'],
            'website': ['icontains'],
            'blood_group': ['icontains'],
            'gender': ['icontains'],
        }


class ProfileListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileListSerializer
    pagination_class = PazeSizePagination
    filterset_class = ProfileFilter

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user.id)


class ProfileRetrieveView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileRetriveSerializer
    lookup_field = "username"

    def get_object(self):
        try:
            return Profile.objects.select_related('user').get(
                user__username=self.kwargs['username']
            )
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        try:
            return Profile.objects.select_related('user').get(
                user__username=self.request.user.username
            )
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


class ProfileImagesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileImagesSerializer
    pagination_class = PazeSizePagination

    def get_queryset(self):
        try:
            user = self.request.user.id
            return Image.objects.filter(author=user)
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)


