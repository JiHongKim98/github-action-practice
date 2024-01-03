from django.core.cache import cache

from .models import Book

BOOKS_CACHE_KEY = 'books'


def cache_all_books():
    all_books = Book.objects.all().select_related('author').values(
        'id',
        'name',
        'author__first_name',
        'author__last_name',
    )
    cache.set(BOOKS_CACHE_KEY, list(all_books))

def get_cached_books():
    return cache.get(BOOKS_CACHE_KEY)
