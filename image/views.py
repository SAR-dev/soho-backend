from django.shortcuts import render
from rest_framework import status, views, permissions, response, parsers, generics
from .serializers import ImageSerializer, ImageCreateSerializer, ImageRetriveSerializer, ImageUpdateSerializer
from .models import Image
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from django_filters import rest_framework as filters

class IsAuthor(permissions.BasePermission):
    message = 'Only author can view this!'
    
    def has_permission(self, request, view):
        try:
            image = Image.objects.get(pk=view.kwargs.get('pk'))
            author = image.author == request.user
            return author
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
        
class ImageFilter(filters.FilterSet):
    o = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
        ),
    )

    class Meta:
        model = Image
        fields = {
            'description': ['icontains'],
            'author__username': ['icontains'],
            'author__first_name': ['icontains'],
            'author__last_name': ['icontains'],
        }
  
class ImageCreateView(generics.CreateAPIView):
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    queryset = Image.objects.all()
    serializer_class = ImageCreateSerializer
        
class ImageRetriveView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Image.objects.all()
    serializer_class = ImageRetriveSerializer
        
class ImageUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthor]
    queryset = Image.objects.all()
    serializer_class = ImageUpdateSerializer