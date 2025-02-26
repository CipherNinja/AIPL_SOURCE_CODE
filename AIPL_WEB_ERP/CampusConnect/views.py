from rest_framework import generics
from .models import CampusConnect
from .serializers import CampusConnectSerializer

class CampusConnectListCreate(generics.ListCreateAPIView):
    queryset = CampusConnect.objects.all()
    serializer_class = CampusConnectSerializer

class CampusConnectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CampusConnect.objects.all()
    serializer_class = CampusConnectSerializer
