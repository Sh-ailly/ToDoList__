from rest_framework import serializers
from .models import todomodel

class TodoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model=todomodel
        fields=['id', 'title', 'description', 'completed', 'user']
