import csv

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients data to database'

    def handle(self, *args, **options):
        with open('recipes/fixtures/ingredients.csv', encoding='Utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    title, dimension = row
                    Ingredient.objects.get_or_create(title=title, dimension=dimension)
                except Exception as exc:
                    print(f'В строке {row} некорректные данные')
