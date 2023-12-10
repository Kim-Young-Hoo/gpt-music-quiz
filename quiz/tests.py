from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Quiz, DifficultyType
import uuid
from rest_framework.test import APIRequestFactory

from .serializers import QuizModelSerializer
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
        serializer = QuizModelSerializer(data=self.quiz_data)
        self.assertTrue(serializer.is_valid())
        quiz_instance = serializer.save()
        self.assertIsInstance(quiz_instance.id, uuid.UUID)
        self.assertEqual(quiz_instance.quiz, "Sample Quiz")

    def test_quiz_serializer_invalid_data(self):
        invalid_data = {
            "quiz": "WRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONG",
            "genre": "WRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONG",
            "difficulty": 'WRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONG',
            "answer": "WRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONG",
            "explanation": "WRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONG",
            "options": "WRONGWRONGWRONGWRONGWRONGWRONGWRONGWRONG"
        }
        serializer = QuizModelSerializer(data=invalid_data)
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

    def test_submit_answer_correct(self):
        view = QuizViewSet.as_view({'post': 'submit_answer'})
        url = reverse('quiz-list') + 'submission/'

        data = {'quiz_id': self.quiz_instance.id, 'answer': '1'}

        request = self.factory.post(url, data, format='json')
        response = view(request)
        is_correct = response.data.get('is_correct', None)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(is_correct, "Response should contain 'is_correct' field")
        self.assertTrue(is_correct, "Expected is_correct to be True for a correct answer")

    def test_submit_answer_incorrect(self):
        view = QuizViewSet.as_view({'post': 'submit_answer'})
        url = reverse('quiz-list') + 'submission/'

        data = {'quiz_id': self.quiz_instance.id, 'answer': '2'}

        request = self.factory.post(url, data, format='json')
        response = view(request)
        is_correct = response.data.get('is_correct', None)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(is_correct, "Response should contain 'is_correct' field")
        self.assertFalse(is_correct, "Expected is_correct to be False for a incorrect answer")


class QuizServiceTestCase(TestCase):
    def setUp(self):
        self.quiz1 = Quiz.objects.create(quiz="Quiz 1",
                                         difficulty=DifficultyType.EASY,
                                         genre="Genre 1",
                                         answer="1",
                                         options={"1": "A", "2": "B", "3": "C"})
        self.quiz2 = Quiz.objects.create(quiz="Quiz 2",
                                         difficulty=DifficultyType.EASY,
                                         genre="Genre 2",
                                         answer="2",
                                         options={"1": "A", "2": "B", "3": "C"})
        self.quiz3 = Quiz.objects.create(quiz="Quiz 3",
                                         difficulty=DifficultyType.EASY,
                                         genre="Genre 3",
                                         answer="3",
                                         options={"1": "A", "2": "B", "3": "C"})

    def test_get_random_quiz(self):
        with patch('quiz.services.choice', return_value=self.quiz2):
            random_quiz = QuizService.get_random_quiz()
        self.assertEqual(random_quiz, self.quiz2)

    def test_get_distinct_genres(self):
        distinct_genres = QuizService.get_distinct_genres()
        expected_genres = ['Genre 1', 'Genre 2', 'Genre 3']
        self.assertEqual(list(distinct_genres), expected_genres)

    def test_get_quiz_by_id_existing_quiz(self):
        quiz_id = self.quiz1.id
        retrieved_quiz = QuizService.get_quiz_by_id(quiz_id)

        self.assertEqual(retrieved_quiz.id, self.quiz1.id)
        self.assertEqual(retrieved_quiz.quiz, self.quiz1.quiz)

    def test_is_correct_answer_correct(self):
        quiz_id = self.quiz1.id
        given_answer = '1'

        is_correct = QuizService.is_correct_answer(quiz_id, given_answer)
        self.assertTrue(is_correct)

    def test_is_correct_answer_incorrect(self):
        quiz_id = self.quiz1.id
        given_answer = '2'

        is_correct = QuizService.is_correct_answer(quiz_id, given_answer)
        self.assertFalse(is_correct)
