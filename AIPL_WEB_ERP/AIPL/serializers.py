# serializers.py
from rest_framework import serializers
from .models import subscribers

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = subscribers
        fields = ['id', 'email', 'created_at']
