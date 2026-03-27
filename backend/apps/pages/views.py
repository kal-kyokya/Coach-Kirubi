from rest_framework.response import Response
from rest_framework.views import APIView
from .models import HomePageContent
from .serializers import HomePageContentSerializer


class HomePageContentAPIView(APIView):
    def get(self, request):
        content, _ = HomePageContent.objects.get_or_create(pk=1)
        serializer = HomePageContentSerializer(content)
        return Response(serializer.data)
