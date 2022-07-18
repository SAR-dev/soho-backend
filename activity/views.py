from django.shortcuts import render
from rest_framework.views import APIView
from utils.paginations import PazeSizePagination
from rest_framework import generics, views, response, permissions, serializers
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django_filters import rest_framework as filters
from django_filters import MultipleChoiceFilter
from activity.models import Activity
from activity.serializers import ActivitySerializer, ActivityNotificationsSerializer
from django.db.models import Count

class ActivityListView(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return Activity.objects.select_related('group').filter(group__author__username=self.kwargs["username"])[:5]
    
class ActivityNotificationsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ActivityNotificationsSerializer
    pagination_class = PazeSizePagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['unread'] = Activity.unread.filter(reciever=request.user).count()
        return response

    def get_queryset(self):
        return Activity.objects.filter(reciever=self.request.user).order_by('done', '-id')
    
class MarkAllNotificationsAsRead(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            Activity.unread.filter(reciever=request.user).update(done=True)
            return response.Response({
                'done': True,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

class MarkSingleNotificationAsRead(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            Activity.unread.filter(reciever=request.user, id=pk).update(done=True)
            return response.Response({
                'done': True,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

class ClapsCounter(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            claps = Activity.objects.filter(reciever=request.user, verb="clapped").count()
            return response.Response({
                'claps': claps,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)