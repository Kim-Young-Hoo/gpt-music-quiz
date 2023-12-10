# In your services.py or managers.py file
from random import choice
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
