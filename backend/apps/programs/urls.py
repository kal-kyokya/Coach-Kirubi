from django.urls import path
from .views import ProgramDetailAPIView, ProgramListAPIView

urlpatterns = [
    path('', ProgramListAPIView.as_view(), name='program-list'),
    path('<slug:slug>/', ProgramDetailAPIView.as_view(), name='program-detail'),
]
