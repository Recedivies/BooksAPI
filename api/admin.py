from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Book

admin.site.site_header = "Books API"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    '''Admin View for Book'''
    list_display = (
        'name',
        'year',
        'author',
        'summary',
        'publisher',
        'pageCount',
        'readPage',
        'reading',
        'insertedAt',
        'updatedAt'
    )


admin.site.unregister(Group)
