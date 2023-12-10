import uuid
from enum import Enum

from django.db import models
from jsonfield import JSONField

from project.base_class.enum_field import EnumField


class DifficultyType(Enum):
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.CharField(max_length=500)
    genre = models.CharField(max_length=20)
    difficulty = EnumField(enum=DifficultyType, max_length=20)
    answer = models.CharField(max_length=5)
    explanation = models.TextField()
    options = JSONField()

    class Meta:
        ordering = ['quiz']
