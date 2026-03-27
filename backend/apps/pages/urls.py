from django.urls import path
from .views import HomePageContentAPIView

urlpatterns = [
    path('home/', HomePageContentAPIView.as_view(), name='home-content'),
]
