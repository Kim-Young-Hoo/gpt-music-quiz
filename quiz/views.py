from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Quiz
from .serializers import QuizModelSerializer, SubmitAnswerSerializer
from .services import QuizService


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizModelSerializer

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
        TODO : 중복 문제가 출제 될 가능성이 있기 때문에 나중에 user relation 맺어서 이미 맞춘 거는 제외하는 로직, 전부 다 맞췄다면 그냥 중복 출제
        """
        random_quiz = QuizService.get_random_quiz()
        serializer = QuizModelSerializer(random_quiz)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_path='submission', serializer_class=SubmitAnswerSerializer)
    def submit_answer(self, request):
        """
        정답 제출 api
        TODO : 정답이 맞을 경우, user-quiz relation에 correct=True하고 user 테이블 correct에 1++ 아닐 경우 그 반대
        """
        quiz_id = request.data.get('quiz_id')
        given_answer = request.data.get('answer')

        if not quiz_id or not given_answer:
            return Response({'error': 'quiz_id and given_answer are required in the request data'},
                            status=status.HTTP_400_BAD_REQUEST)

        is_correct = QuizService.is_correct_answer(quiz_id, given_answer)
        response_data = {'quiz_id': quiz_id, 'given_answer': given_answer, 'is_correct': is_correct}
        return Response(response_data, status=status.HTTP_200_OK)
