from django.urls import include, path
from django.contrib import admin
from project import settings


api_prefix = f'api/{settings.API_VERSION}/'


urlpatterns = [
    path('admin/', admin.site.urls),
    path(api_prefix, include('quiz.urls')),
]

