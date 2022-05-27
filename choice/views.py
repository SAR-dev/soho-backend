from django.shortcuts import render
from rest_framework import status, views, permissions, response, parsers, generics
from .serializers import ChoiceSerializer, ChoiceCreateSerializer, ChoiceRetriveSerializer, ChoiceUpdateSerializer
from .models import Choice
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from django_filters import rest_framework as filters

class IsAuthor(permissions.BasePermission):
    message = 'Only author can view this!'
    
    def has_permission(self, request, view):
        try:
            obj = Choice.objects.get(id=view.kwargs.get('pk'))
            author = obj.author == request.user
            return author
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
  
class ChoiceCreateView(generics.CreateAPIView):
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    permission_classes = [permissions.IsAuthenticated]
    queryset = Choice.objects.all()
    serializer_class = ChoiceCreateSerializer
        
class ChoiceRetriveView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Choice.objects.all()
    serializer_class = ChoiceRetriveSerializer
        
class ChoiceUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthor]
    queryset = Choice.objects.all()
    serializer_class = ChoiceUpdateSerializer