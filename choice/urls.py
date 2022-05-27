from django.urls import path
from .views import ChoiceCreateView, ChoiceRetriveView, ChoiceUpdateView

app_name = 'choice'

urlpatterns = [
    path('create/', ChoiceCreateView.as_view(), name='choice-create'),
    path('<int:pk>/', ChoiceRetriveView.as_view(), name='choice-retrive'),
    path('<int:pk>/update/', ChoiceUpdateView.as_view(), name='choice-update')
]