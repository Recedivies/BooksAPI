from django.contrib import admin

from .models import Book

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