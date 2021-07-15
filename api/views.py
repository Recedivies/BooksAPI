from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.filters import BooksFilter
from api.models import Book
from api.serializers import (
    AddBookSerializer,
    ListBookSerializer,
    ListBookByIdSerializer,
    UpdateBookSerializer,
)


def inValidPage(request):
    readPage = int(request.data['readPage'])
    pageCount = int(request.data['pageCount'])
    return readPage > pageCount


def responseReadPageGreaterThanPageCount():
    return Response({
        "status": "fail",
        "message": "Gagal menambahkan buku. readPage tidak boleh lebih besar dari pageCount"
    }, status=status.HTTP_400_BAD_REQUEST)


def responseNoName():
    return Response({
        "status": "fail",
        "message": "Gagal menambahkan buku. Mohon isi nama buku"
    }, status=status.HTTP_400_BAD_REQUEST)


def responseNoId(info):
    return Response({
        "status": "fail",
        "message": f"{info}. Id tidak ditemukan"
    }, status=status.HTTP_404_NOT_FOUND)


class ListCreateBook(ListCreateAPIView):
    """
    Allowed methods: GET, POST
    GET   books - lists all Books with query_params
    POST  books - add book with given content
    """
    queryset = Book.objects.all()
    serializer_class = AddBookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = BooksFilter

    def get(self, request, *args, **kwargs):
        books = self.filter_queryset(self.get_queryset())
        serializer = ListBookSerializer(instance=books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if (request.data['name'] == ''):
            return responseNoName()

        if (inValidPage(request)):
            return responseReadPageGreaterThanPageCount()

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
    Allowed methods: GET, PUT, PATCH, DELETE
    GET    books/<id>/ - List Book by id
    PUT    books/<id>/ - Edit Entire Book by id
    PATCH  books/<id>/ - Edit Partial Book by id
    DELETE books/<id>/ - Delete Book by id
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
            return responseNoId("Gagal mendapatkan data buku")

    def put(self, request, pk):
        if (request.data['name'] == ''):
            return responseNoName()

        if (inValidPage(request)):
            return responseReadPageGreaterThanPageCount()

        try:
            book = Book.objects.get(pk=pk)
            serializer = UpdateBookSerializer(book, data=request.data)
            if (serializer.is_valid()):
                serializer.save()
        except Book.DoesNotExist:
            return responseNoId("Gagal memperbarui buku")

        return Response({
            "status": "success",
            "message": "Buku berhasil diperbarui"
        }, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        if (request.data.get('name') is not None and request.data['name'] == ''):
            return responseNoName()

        if (request.data.get('readPage') is not None and request.data.get('pageCount') is not None):
            if (inValidPage(request)):
                return responseReadPageGreaterThanPageCount()

        try:
            book = Book.objects.get(pk=pk)
            serializer = UpdateBookSerializer(
                book, data=request.data, partial=True)
            if (serializer.is_valid()):
                serializer.save()
        except Book.DoesNotExist:
            return responseNoId("Gagal memperbarui buku")

        return Response({
            "status": "success",
            "message": "Buku berhasil diperbarui"
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
        except Book.DoesNotExist:
            return responseNoId("Buku gagal dihapus")

        return Response({
            "status": "success",
            "message": "Buku berhasil dihapus"
        }, status=status.HTTP_200_OK)
