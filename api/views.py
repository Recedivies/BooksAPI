from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Book
from api.serializers import (
    AddBookSerializer,
    ListBookSerializer,
    ListBookByIdSerializer,
    UpdateBookSerializer,
    DeleteBookSerializer,
)


class ListCreateBook(ListCreateAPIView):
    """
    Allowed methods: GET, POST
    GET   books - lists all Books with query_params
    POST  books - add book with given content
    """
    queryset = Book.objects.all()
    serializer_class = ListBookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        books = Book.objects.all()
        serializer = ListBookSerializer(instance=books, many=True)
        # try:
        #     reading = request.query_params['reading']
        #     if (reading is not None):
        #         books = Book.objects.filter(reading=reading)
        #         serializer = ListBookSerializer(books, many=True)
        # except (KeyError, Book.DoesNotExist):
        #     try:
        #         finished = request.query_params['finished']
        #         if (finished is not None):
        #             books = Book.objects.filter(finished=finished)
        #             serializer = ListBookSerializer(books, many=True)
        #     except (KeyError, Book.DoesNotExist):
        #         books = Book.objects.all()
        #         serializer = ListBookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if (request.data['name'] == ''):
            return Response({
                "status": "fail",
                "message": "Gagal menambahkan buku. Mohon isi nama buku"
            }, status=status.HTTP_400_BAD_REQUEST)

        readPage = request.data['readPage']
        pageCount = request.data['pageCount']
        if (int(readPage) > int(pageCount)):
            return Response({
                "status": "fail",
                "message": "Gagal menambahkan buku. readPage tidak boleh lebih besar dari pageCount"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = AddBookSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response({
                "status": "success",
                "message": "Buku berhasil ditambahkan",
                "data": {
                    "bookId": serializer.data['id']
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "message": "Buku gagal ditambahkan"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListUpdateDeleteBookById(RetrieveUpdateDestroyAPIView):
    """
    Allowed methods: GET, PUT, DELETE
    GET    books/<id> - List Book by id
    PUT    books/<id> - Edit Book by id
    DELETE books/<id> - Delete Book by id
    """
    queryset = Book.objects.all()
    serializer_class = UpdateBookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = ListBookByIdSerializer(book, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({
                "status": "fail",
                "message": "Buku tidak ditemukan"
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        if (request.data['name'] == ''):
            return Response({
                "status": "fail",
                "message": "Gagal memperbarui buku. Mohon isi nama buku"
            }, status=status.HTTP_400_BAD_REQUEST)

        readPage = request.data['readPage']
        pageCount = request.data['pageCount']
        if (int(readPage) > int(pageCount)):
            return Response({
                "status": "fail",
                "message": "Gagal menambahkan buku. readPage tidak boleh lebih besar dari pageCount"
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.get(pk=pk)
            serializer = UpdateBookSerializer(book, data=request.data)
            if (serializer.is_valid()):
                serializer.save()
        except Book.DoesNotExist:
            return Response({
                "status": "fail",
                "message": "Gagal memperbarui buku. Id tidak ditemukan"
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": "success",
            "message": "Buku berhasil diperbarui"
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
        except Book.DoesNotExist:
            return Response({
                "status": "fail",
                "message": "Buku gagal dihapus. Id tidak ditemukan"
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": "success",
            "message": "Buku berhasil dihapus"
        }, status=status.HTTP_200_OK)
