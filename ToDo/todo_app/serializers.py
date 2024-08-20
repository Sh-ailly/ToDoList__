from rest_framework import serializers
from .models import todomodel

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model=todomodel
        fields=['id', 'title', 'description', 'completed']
