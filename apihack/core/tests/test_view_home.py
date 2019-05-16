from django.test import TestCase
from apihack.core.models import Book, Author
from apihack.core.views import home
from django.core.serializers import serialize
from pprint import pprint


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

        self.xml_author = f'<?xml version="1.0" encoding="utf-8"?>\n<django-objects version="1.0"><object model="core.author" pk="{self.author.pk}"><field name="name" type="CharField">{self.author.name}</field><field name="age" type="IntegerField">{self.author.age}</field></object></django-objects>'


        self.xml_book = f'<?xml version="1.0" encoding="utf-8"?>\n<django-objects version="1.0"><object model="core.book" pk="{self.book.pk}"><field name="author" rel="ManyToOneRel" to="core.author">{self.book.author.pk}</field><field name="title" type="CharField">{self.book.title}</field><field name="pages" type="IntegerField">{self.book.pages}</field></object></django-objects>'

        self.response_author = self.client.get(f"/core/author/{self.author.pk}/")
        self.response_book = self.client.get(f"/core/book/{self.book.pk}/")
        self.response_author_xml = self.client.get(f"/core/author/{self.author.pk}/?fmt=xml")
        self.response_book_xml = self.client.get(f"/core/book/{self.book.pk}/?fmt=xml")



    def test_get_home_author(self):
        self.assertEqual(200, self.response_author.status_code)

    def test_get_home_book(self):
        self.assertEqual(200, self.response_book.status_code)

    def test_json_serialized_author(self):
        '''test serialize json data author'''
        author_serialized = serialize('json', Author.objects.all())
        self.assertJSONEqual(author_serialized, self.json_author)

    def test_json_serialized_book(self):
        '''test serialize json data book'''
        book_serialized = serialize('json', Book.objects.all())
        self.assertJSONEqual(book_serialized, self.json_book)

    def test_json_author(self):
        '''GET /core/author/1/ de retornar json'''
        self.assertJSONEqual(self.response_author.content, self.json_author)

    def test_json_book(self):
        '''GET /core/book/1/ de retornar json'''
        self.assertJSONEqual(self.response_book.content, self.json_book)

    def test_xml_serialized_author(self):
        '''test serialize xml_ data author'''
        author_serialized = serialize('xml', Author.objects.all())

        self.assertXMLEqual(author_serialized, self.xml_author)

    def test_xml_serialized_book(self):
        '''test serialize xml_ data book'''
        book_serialized = serialize('xml', Book.objects.all())
        self.assertXMLEqual(book_serialized, self.xml_book)




