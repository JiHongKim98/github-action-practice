import random
from django.test import TestCase
from rest_framework.test import APITestCase

from api.models import Author, Book
from api.utils import cache_all_books, get_cached_books


class CacheTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author_1 = Author.objects.create(first_name='Kim', last_name='Ji-hong')
        cls.author_2 = Author.objects.create(first_name='Dummy', last_name='Dummy-name')
        authors = [cls.author_1, cls.author_2]

        cls.books = Book.objects.bulk_create([
            Book(name=f'number {_}', author=random.choice(authors)) for _ in range(10000)
        ])

    def test_cached_books(self):
        initial_book_ids = [_.id for _ in self.books]

        cache_all_books()
        cached_books = get_cached_books()
        cached_book_ids = [_['id'] for _ in cached_books]

        self.assertListEqual(initial_book_ids, cached_book_ids)


class BookCreateTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(first_name='Kim', last_name='Ji-hong')

    def test_create_book(self):
        response = self.client.post(
            path="/api/v1/books/",
            data={
                "name": "name",
                "author": self.author.pk
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 1)
