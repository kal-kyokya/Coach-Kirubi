from rest_framework import serializers
from .models import HomePageContent


class HomePageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageContent
        fields = '__all__'
