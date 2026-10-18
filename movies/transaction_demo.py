
from django.db import transaction

from .models import Movie, Review


def update_movie_and_create_review(movie_id):
    try:
        with transaction.atomic():
            movie = Movie.objects.get(id=movie_id)

            movie.title = 'Новое название фильма'
            movie.is_published = True
            movie.save()

            Review.objects.create(
                movie=movie,
                author='Тестовый автор',
                text='Это тестовый отзыв.',
                rating=5
            )

            raise ValueError('Искусственная ошибка')

    except ValueError as error:
        print('Транзакция отменена:', error)
