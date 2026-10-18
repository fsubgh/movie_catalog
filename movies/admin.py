from django.contrib import admin

# Register your models here.

from django.utils.html import format_html

from .models import Movie, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'release_year',
        'is_published',
        'created_at',
    )

    search_fields = ('title', 'description')
    list_filter = ('is_published', 'release_year')

    readonly_fields = (
        'created_at',
        'poster_preview',
        'file_link',
    )

    inlines = [ReviewInline]

    @admin.display(description='Предпросмотр постера')
    def poster_preview(self, obj):
        if obj and obj.poster:
            return format_html(
                '<img src="{}" width="150">',
                obj.poster.url
            )
        return 'Постер не загружен'

    @admin.display(description='Дополнительный файл')
    def file_link(self, obj):
        if obj and obj.file:
            return format_html(
                '<a href="{}" target="_blank">Открыть или скачать файл</a>',
                obj.file.url
            )
        return 'Файл не загружен'

    @admin.action(description='Опубликовать выбранные фильмы')
    def publish_movies(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description='Снять выбранные фильмы с публикации')
    def unpublish_movies(self, request, queryset):
        queryset.update(is_published=False)

    actions = ['publish_movies', 'unpublish_movies']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'movie', 'rating', 'created_at')
    search_fields = ('author', 'text', 'movie__title')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('created_at',)
