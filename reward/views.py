from rest_framework.views import APIView
from .models import Reward
from rest_framework import generics, views, response, permissions, serializers
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist

class RewardPointsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            auth_user = self.request.user
            reward = Reward.objects.get(author__id = auth_user.id)
            return response.Response({
                'score': reward.total_score,
            })
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
