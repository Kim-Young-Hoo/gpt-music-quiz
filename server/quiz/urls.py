from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(prefix=r'quiz', viewset=views.QuizViewSet)

urlpatterns = [
    path('', include(router.urls)),
]