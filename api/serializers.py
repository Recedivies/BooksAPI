from rest_framework import serializers

from .models import Book

class ListBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('__all__')
        # fields = ('id', 'name', 'publisher')

class ListBookByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class AddBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('__all__'
        # 'id', 
        # 'name', 
        # 'year', 
        # 'author', 
        # 'summary', 
        # 'publisher', 
        # 'pageCount', 
        # 'readPage', 
        # 'finished',
        # 'reading'
        )
        read_only_fields = ('id', )

class UpdateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
        'name', 
        'year', 
        'author', 
        'summary', 
        'publisher', 
        'pageCount', 
        'readPage', 
        'reading'
        )

class DeleteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book