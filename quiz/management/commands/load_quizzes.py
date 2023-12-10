# management/commands/load_quizzes.py
import json
from django.core.management.base import BaseCommand
from quiz.models import Quiz

json_dummy_file_path = './data/quiz.json'


class Command(BaseCommand):
    help = 'Load quizzes from JSON file and insert into the database'

    def handle(self, *args, **options):
        with open(json_dummy_file_path, 'r') as json_file:
            data = json.load(json_file)

            for quiz_data in data:
                Quiz.objects.create(**quiz_data)
        self.stdout.write(self.style.SUCCESS('Successfully loaded quizzes into the database.'))
