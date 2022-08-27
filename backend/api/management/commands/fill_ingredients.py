import csv
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from api.models import Ingredient

User = get_user_model()
DATA_DIR = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Наполняет таблицы БД данными из CSV-таблиц'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.add_users()
        self.stdout.write(self.style.SUCCESS('Данные добавлены'))

    def get_csv_reader(self, name):
        """Загружает таблицу по имени (расширение передавать не требуется)"""
        path = os.path.join(DATA_DIR, name) + '.csv'
        f = open(path, 'r', encoding='utf-8')
        print(path)
        return csv.DictReader(f)

    def add_users(self):
        reader = self.get_csv_reader('ingredients')
        ingredients = []
        id = 0 #Небольшой костыль, ибо в файле не было столбца id
        for row in reader:
            id += 1
            ingredients.append(Ingredient(id=id, **row))
        Ingredient.objects.bulk_create(ingredients)
