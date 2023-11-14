from csv import DictReader
from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User

MODEL_CSV = {
    'static/data/users.csv': User,
    'static/data/category.csv': Category,
    'static/data/genre.csv': Genre,
    'static/data/titles.csv': Title,
    'static/data/genre_title.csv': Title.genre.through,
    'static/data/review.csv': Review,
    'static/data/comments.csv': Comment,
}


class Command(BaseCommand):
    """Загрузчик данных csv. """

    help = 'Import .csv files'

    def handle(self, *args, **options):
        for csv, model in MODEL_CSV.items():
            # model.objects.all().delete() Если нужно
            # все очистить, включая удаление superuser
            with open(f'{settings.BASE_DIR}/static/data/{csv}',
                      'r', encoding='utf-8') as csv_file:
                reader = DictReader(csv_file)
                for row in reader:
                    if 'category' in row:
                        row['category_id'] = row['category']
                        del row['category']
                    if 'author' in row:
                        row['author_id'] = row['author']
                        del row['author']
                    model.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS('Данные из .csv '
                                             'файлов загружены успешно!'))
