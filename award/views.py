from .models import Award
from .serializers import AwardListSerializer, AwardCreateSerializer, AwardUpdateSerializer
from rest_framework import generics, views, response, permissions, serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from django.db.models import Q


class IsAuthor(permissions.BasePermission):
    message = 'Only author can view this!'
    
    def has_permission(self, request, view):
        try:
            obj = Award.objects.get(id=view.kwargs.get('pk'))
            author = obj.author == request.user
            return author
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)

class AwardCreateView(generics.CreateAPIView):
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    permission_classes = [permissions.IsAuthenticated]
    queryset = Award.objects.all()
    serializer_class = AwardCreateSerializer

class AwardUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthor]
    queryset = Award.objects.all()
    serializer_class = AwardUpdateSerializer
    
class GroupAwardListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AwardListSerializer

    def get_queryset(self):
        return Award.objects.select_related('author').filter(Q(author__username=self.kwargs["username"]) | Q(public=True))

class UserAwardListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AwardListSerializer

    def get_queryset(self):
        return Award.objects.select_related('author').filter(author__username=self.kwargs["username"])