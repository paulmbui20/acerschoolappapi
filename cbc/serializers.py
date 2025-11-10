from rest_framework import serializers
from .models import LearningArea, LearningLevel


class LearningAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningArea
        fields = ["id", "name", "code"]


class LearningLevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningLevel
        fields = ["id", "name"]
