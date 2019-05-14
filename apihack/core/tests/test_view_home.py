from django.test import TestCase
from apihack.core.models import Book, Author
from apihack.core.views import home
from django.core.serializers import serialize


class ViewHomeTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Octavio', age=22)
        self.book = Book.objects.create(author=self.author, title='Fernao Capelo', pages=300)
        self.json_author = [{
            "model": "core.author",
            "pk": self.author.pk,
            "fields": {"name": self.author.name, "age": self.author.age}}]

        self.json_book = [{
            "model": "core.book",
            "pk": self.book.pk,
            "fields": {"author": self.author.pk, "title": self.book.title, "pages": self.book.pages}
        }]

        self.response_author = self.client.get(f"/core/author/{self.author.pk}/")
        self.response_book = self.client.get(f"/core/book/{self.book.pk}/")

    def test_get_home_author(self):
        self.assertEqual(200, self.response_author.status_code)

    def test_get_home_book(self):
        self.assertEqual(200, self.response_book.status_code)

    def test_serialized_author(self):
        '''test serialize data author'''
        author_serialized = serialize('json', Author.objects.all())
        self.assertJSONEqual(author_serialized, self.json_author)

    def test_serialized_book(self):
        '''test serialize data book'''
        book_serialized = serialize('json', Book.objects.all())
        self.assertJSONEqual(book_serialized, self.json_book)

    def test_json_author(self):
        '''GET /core/author/1/ de retornar json'''
        print(self.response_author)
        #self.assertJSONEqual(self.response_author.GET(), self.json_author)