from django.shortcuts import render
from rest_framework import status, views, permissions, response, parsers, generics
from .serializers import AdvertisementRetriveSerializer, AdvertisementUpdateSerializer
from .models import Advertisement
from group.models import Group
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound

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

class IsAuthor(permissions.BasePermission):
    message = 'Only author can view this!'
    
    def has_permission(self, request, view):
        try:
            obj = Advertisement.objects.select_related('author').get(author__username=view.kwargs.get('username'))
            author = obj.author == request.user
            return author
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

class AdvertisementRetriveView(generics.RetrieveAPIView):
    # permission_classes = [IsGroupSubscriber]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AdvertisementRetriveSerializer

    def get_object(self):
        try:
            ad = Advertisement.objects.select_related('author').get(author__username=self.kwargs['username'])
            return ad
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

class AdvertisementUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthor]
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementUpdateSerializer

    def get_object(self):
        try:
            ad = Advertisement.objects.select_related('author').get(author__username=self.kwargs['username'])
            return ad
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)