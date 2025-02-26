from rest_framework import serializers
from .models import CampusConnect

class CampusConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusConnect
        fields = '__all__'
