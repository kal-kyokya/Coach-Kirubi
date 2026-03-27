from rest_framework import generics
from .models import Program
from .serializers import ProgramSerializer


class ProgramListAPIView(generics.ListAPIView):
    serializer_class = ProgramSerializer

    def get_queryset(self):
        return Program.objects.filter(is_published=True)


class ProgramDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProgramSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Program.objects.filter(is_published=True)
