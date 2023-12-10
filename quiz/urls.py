from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(prefix=r'quiz', viewset=views.QuizViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/quiz/distinct-genres/', views.QuizViewSet.as_view({'get': 'distinct_genres'}), name='distinct-genres'),
    path('api/v1/quiz/random/', views.QuizViewSet.as_view({'get': 'random'}), name='random'),
]