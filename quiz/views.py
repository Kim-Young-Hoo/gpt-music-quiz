from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Quiz
from .serializers import QuizSerializer
from .services import QuizService


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_queryset(self):
        queryset = Quiz.objects.all()
        genre = self.request.query_params.get('genre', None)
        if genre is not None:
            queryset = queryset.filter(genre=genre)
        return queryset

    @action(detail=False, methods=['GET'], url_path='distinct-genres')
    def get_distinct_genres(self, request):
        """
        퀴즈 장르 목록 나열
        django는 order by 하지 않으면 distinct 쿼리가 먹히지 않는다 함...
        참고 : https://velog.io/@paori/django-%EC%BF%BC%EB%A6%AC%EC%85%8B-%EC%A4%91%EB%B3%B5%EC%A0%9C%EA%B1%B0-distinct-%EC%95%88%EB%90%A8
        """
        return Response(QuizService.get_distinct_genres())

    @action(detail=False, methods=['GET'], url_path='random')
    def get_random_quiz(self, request):
        """
        id가 uuid이기 때문에 만드는 random 함수
        TODO : 중복 문제가 출제 될 가능성이 있기 때문에 나중에 user relation 맺어서 중복 없애야 함
        """
        random_quiz = QuizService.get_random_quiz()
        serializer = QuizSerializer(random_quiz)
        return Response(serializer.data)
