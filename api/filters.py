import django_filters as filters
from api.models import Book


class BooksFilter(filters.FilterSet):

    class Meta:
        model = Book
        fields = ['name', 'reading', 'finished']
