from rest_framework import serializers
from .models import Quiz


class QuizModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'quiz', 'genre', 'difficulty', 'options',)


class SubmitAnswerSerializer(serializers.Serializer):
    quiz_id = serializers.CharField()
    answer = serializers.CharField()
