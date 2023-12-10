# In your services.py or managers.py file
from random import choice

from django.shortcuts import get_object_or_404

from .models import Quiz


class QuizService:
    @staticmethod
    def get_random_quiz():
        queryset = Quiz.objects.all()
        random_quiz = choice(queryset)
        return random_quiz

    @staticmethod
    def get_distinct_genres():
        return Quiz.objects.all().values_list('genre', flat=True).distinct().order_by('genre')

    @staticmethod
    def get_quiz_by_id(id):
        return get_object_or_404(Quiz, id=id)

    @staticmethod
    def is_correct_answer(quiz_id, given_answer):
        quiz = QuizService.get_quiz_by_id(quiz_id)
        return quiz.answer == given_answer