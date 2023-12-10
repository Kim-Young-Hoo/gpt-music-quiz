from rest_framework import serializers
from .models import Quiz


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'quiz', 'genre', 'difficulty', 'options',)


class SubmitAnswerDTO(serializers.Serializer):
    quiz_id = serializers.CharField()
    answer = serializers.CharField()
