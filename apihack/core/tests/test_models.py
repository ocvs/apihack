from django.test import TestCase
from apihack.core.models import Book, Author


class ModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Octavio', age=22)
        self.book = Book.objects.create(author=self.author, title='Fernão Capelo', pages=300)

    def test_author_create(self):
        self.assertTrue(Author.objects.exists())

    def test_book_create(self):
        self.assertTrue(Book.objects.exists())

    def test_author_have_book(self):
        self.assertEqual(1, self.author.books.count())
