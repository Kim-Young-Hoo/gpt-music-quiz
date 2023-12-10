import uuid
from enum import Enum

from django.db import models
from enumfields import EnumField
from jsonfield import JSONField


class Difficulty(Enum):
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.CharField(max_length=500)
    genre = models.CharField(max_length=20)
    difficulty = EnumField(Difficulty)
    answer = models.CharField(max_length=5)
    explanation = models.TextField()
    options = JSONField()

    class Meta:
        ordering = ['quiz']
