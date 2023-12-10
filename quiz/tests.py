from unittest.mock import patch

from django.test import TestCase
from .models import Quiz, DifficultyType
import uuid
from rest_framework.test import APIRequestFactory

from .serializers import QuizSerializer
from .services import QuizService
from .views import QuizViewSet


class QuizModelTestCase(TestCase):
    def setUp(self):
        Quiz.objects.create(
            quiz="Sample Quiz",
            genre="Sample Genre",
            difficulty="Easy",
            answer="1",
            explanation="Sample Explanation",
            options={"1": "A", "2": "B", "3": "C", "4": "C"}
        )

    def test_quiz_model_creation(self):
        quiz = Quiz.objects.first()
        self.assertEqual(quiz.quiz, "Sample Quiz")
        self.assertEqual(quiz.genre, "Sample Genre")
        self.assertEqual(quiz.difficulty, DifficultyType.EASY.value)
        self.assertEqual(quiz.answer, "1")
        self.assertEqual(quiz.explanation, "Sample Explanation")
        self.assertEqual(quiz.options, {"1": "A", "2": "B", "3": "C", "4": "C"})
        self.assertIsInstance(quiz.id, uuid.UUID)


class QuizSerializerTestCase(TestCase):
    def setUp(self):
        self.quiz_data = {
            "quiz": "Sample Quiz",
            "genre": "Sample Genre",
            "difficulty": 'Easy',
            "answer": "1",
            "explanation": "Sample Explanation",
            "options": {"1": "A", "2": "B", "3": "C", "4": "C"}
        }

    def test_quiz_serializer_valid_data(self):
        serializer = QuizSerializer(data=self.quiz_data)
        self.assertTrue(serializer.is_valid())
        quiz_instance = serializer.save()
        self.assertIsInstance(quiz_instance.id, uuid.UUID)
        self.assertEqual(quiz_instance.quiz, "Sample Quiz")

    def test_quiz_serializer_invalid_data(self):
        invalid_data = {
            "quiz": "Sample Quiz",
            "genre": "Sample Genre",
            "difficulty": 'WRONG',
            "answer": "WRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONG",
            "explanation": "Sample Explanation",
            "options": "WRONG"
        }
        serializer = QuizSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class QuizViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.quiz_data = {
            "quiz": "Sample Quiz",
            "genre": "Sample Genre",
            "difficulty": DifficultyType.EASY.value,
            "answer": "1",
            "explanation": "Sample Explanation",
            "options": {"1": "A", "2": "B", "3": "C"}
        }
        self.quiz_instance = Quiz.objects.create(**self.quiz_data)

    def test_get_queryset(self):
        view = QuizViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/quiz/', {'genre': 'Sample Genre'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_get_distinct_genres(self):
        view = QuizViewSet.as_view({'get': 'get_distinct_genres'})
        request = self.factory.get('/api/v1/quiz/distinct-genres/')
        response = view(request)
        self.assertEqual(response.status_code, 200)


class QuizServiceTestCase(TestCase):
    def setUp(self):
        self.quiz1 = Quiz.objects.create(quiz="Quiz 1", difficulty=DifficultyType.EASY, genre="Genre 1", options={})
        self.quiz2 = Quiz.objects.create(quiz="Quiz 2", difficulty=DifficultyType.EASY, genre="Genre 2", options={})
        self.quiz3 = Quiz.objects.create(quiz="Quiz 3", difficulty=DifficultyType.EASY, genre="Genre 3", options={})

    def test_get_random_quiz(self):
        with patch('quiz.services.choice', return_value=self.quiz2):
            random_quiz = QuizService.get_random_quiz()

        self.assertEqual(random_quiz, self.quiz2)

    def test_get_distinct_genres(self):
        distinct_genres = QuizService.get_distinct_genres()
        expected_genres = ['Genre 1', 'Genre 2', 'Genre 3']
        self.assertEqual(list(distinct_genres), expected_genres)
