from rest_framework import serializers
from .models import Program


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            'id',
            'title',
            'slug',
            'short_description',
            'description',
            'price',
            'duration_weeks',
            'level',
            'delivery_format',
            'thumbnail_url',
            'is_featured',
        ]
