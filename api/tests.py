from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Book

from django.contrib.auth.models import User
from django.utils import timezone


class BooksAPIViewTests(APITestCase):
    BASE_URL = "http://127.0.0.1:8000/api"
    AUTH_URL = "http://127.0.0.1:8000/api/auth"

    def setUp(self) -> None:
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username='test', password='Rcd320112',
                                       email='test@gmail.com', first_name='test', last_name='123')

    @property
    def bearer_token(self):
        """Returns Authorization headers, which can be passed to APIClient instance."""
        refresh = RefreshToken.for_user(self.user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}

    @property
    def create_book_with_complete_data(self):
        book = Book.objects.create(
            name="Recedivies",
            year=2020,
            author="Rois",
            summary="Nice",
            publisher="Tono",
            pageCount=400,
            readPage=200,
            finished=False,
            reading=False,
        )
        return book

    @property
    def book_with_complete_data(self):
        data = {
            "name": "Recedivies",
            "year": 2020,
            "author": "Rois",
            "summary": "Nice",
            "publisher": "Tono",
            "pageCount": 400,
            "readPage": 200,
            "finished": False,
            "reading": False,
            "insertedAt": timezone.now(),
            "updatedAt": timezone.now(),
        }
        return data

    @property
    def book_without_name(self):
        data = {
            "name": "",
            "year": 2020,
            "author": "Rois",
            "summary": "Nice",
            "publisher": "Tono",
            "pageCount": 400,
            "readPage": 200,
            "finished": False,
            "reading": False,
            "insertedAt": timezone.now(),
            "updatedAt": timezone.now(),
        }
        return data

    @property
    def book_with_page_read_more_than_page_count(self):
        data = {
            "name": "Recedivies",
            "year": 2020,
            "author": "Rois",
            "summary": "Nice",
            "publisher": "Tono",
            "pageCount": 400,
            "readPage": 401,
            "finished": False,
            "reading": False,
            "insertedAt": timezone.now(),
            "updatedAt": timezone.now(),
        }
        return data

    def test_is_authenticated(self):
        """Test views with required authorization"""
        url = f"{self.BASE_URL}/books/"
        book = self.create_book_with_complete_data
        data = self.book_with_complete_data
        url_id = f"{self.BASE_URL}/books/{book.id}/"

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(url_id, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(url_id, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_change_password(self):
    #     user_id = self.user.id
    #     url = f"{self.AUTH_URL}/password/{user_id}/"
    #     data = {
    #         "password": "rcd320112",
    #         "password2": "rcd320112",
    #         "old_password": f"{self.user.password}"
    #     }

    #     response = self.client.put(url, data, format="json", **self.bearer_token)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(self.user.password, data.password)

    def test_wrong_method(self):
        """Test ListCreateBook with not allowed methods"""
        url = f"{self.BASE_URL}/books/"

        response = self.client.delete(url, **self.bearer_token)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url, **self.bearer_token)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(url, **self.bearer_token)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_book_with_complete_data(self):
        url = f"{self.BASE_URL}/books/"
        data = self.book_with_complete_data
        response = self.client.post(
            url, data, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_without_name(self):
        url = f"{self.BASE_URL}/books/"
        data = self.book_without_name
        response = self.client.post(
            url, data, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_with_page_read_more_than_page_count(self):
        url = f"{self.BASE_URL}/books/"
        data = self.book_with_page_read_more_than_page_count
        response = self.client.post(
            url, data, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_books(self):
        url = f"{self.BASE_URL}/books/"
        response = self.client.get(url, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_book_with_correct_id(self):
        book = self.create_book_with_complete_data
        url = f"{self.BASE_URL}/books/{book.id}/"
        response = self.client.get(url, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_book_with_invalid_id(self):
        url = f"{self.BASE_URL}/books/xxxxxxxx/"
        response = self.client.get(url, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_book_with_complete_data(self):
        book = self.create_book_with_complete_data
        updated_data = self.book_with_complete_data
        url = f"{self.BASE_URL}/books/{book.id}/"
        response = self.client.put(
            url, updated_data, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_book_without_name(self):
        book = self.create_book_with_complete_data
        updated_data = self.book_without_name
        url = f"{self.BASE_URL}/books/{book.id}/"
        response = self.client.put(
            url, updated_data, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book_with_page_read_more_than_page_count(self):
        book = self.create_book_with_complete_data
        updated_data = self.book_with_page_read_more_than_page_count
        url = f"{self.BASE_URL}/books/{book.id}/"
        response = self.client.put(
            url, updated_data, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book_with_invalid_id(self):
        updated_data = self.book_with_complete_data
        url = f"{self.BASE_URL}/books/xxxxx/"
        response = self.client.put(
            url, updated_data, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_correct_id(self):
        book = self.create_book_with_complete_data
        url = f"{self.BASE_URL}/books/{book.id}/"
        response = self.client.delete(url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_with_invalid_id(self):
        url = f"{self.BASE_URL}/books/xxxxx/"
        response = self.client.delete(url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_get_book_with_create_unfinished_book(self):
        url = f"{self.BASE_URL}/books/"
        data = self.book_with_complete_data
        response = self.client.post(url, data, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.filter(finished=False).count(), 1)
        self.assertEqual(Book.objects.filter(finished=True).count(), 0)

    def test_filter_create_unreading_book(self):
        url = f"{self.BASE_URL}/books/"
        data = self.book_with_complete_data
        data['reading'] = False
        response = self.client.post(url, data, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.filter(reading=True).count(), 0)
        self.assertEqual(Book.objects.filter(reading=False).count(), 1)
