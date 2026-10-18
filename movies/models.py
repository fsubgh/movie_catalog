from django.db import models

# Create your models here.

from PIL import Image


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    release_year = models.PositiveIntegerField(verbose_name='Год выпуска')

    poster = models.ImageField(
        upload_to='posters/',
        blank=True,
        null=True,
        verbose_name='Постер'
    )

    file = models.FileField(
        upload_to='files/',
        blank=True,
        null=True,
        verbose_name='Дополнительный файл'
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликован'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.poster:
            try:
                with Image.open(self.poster.path) as image:
                    if image.width > 1200 or image.height > 1200:
                        image.thumbnail((1200, 1200))
                        image.save(self.poster.path)
            except (OSError, ValueError):
                pass

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['-created_at']


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Фильм'
    )

    author = models.CharField(max_length=100, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст отзыва')

    rating = models.PositiveSmallIntegerField(
        choices=[
            (1, '1 — Очень плохо'),
            (2, '2 — Плохо'),
            (3, '3 — Нормально'),
            (4, '4 — Хорошо'),
            (5, '5 — Отлично'),
        ],
        verbose_name='Оценка'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'{self.author} — {self.movie.title}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
