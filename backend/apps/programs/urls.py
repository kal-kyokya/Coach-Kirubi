from django.urls import path
from .view import ProgramDetailAPIView, ProgramListAPIView

urlpartters = [
    path('', ProgramListAPIView.as_view(), name='program-list'),
    path('<slug:slug>/', ProgramDetailAPIView.as_view(), name='program-detail'),
]
