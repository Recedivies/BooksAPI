from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Book

from django.utils import timezone

import json

class BooksAPIViewTests(APITestCase):
  BASE_URL = "http://127.0.0.1:8000"

  def test_create_book_with_complete_data(self):
    url = f"{self.BASE_URL}/books/"
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
    response = self.client.post(url, data, format="json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
  
  def test_create_book_without_name(self):
    url = f"{self.BASE_URL}/books/"
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
    response = self.client.post(url, data, format="json")
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_add_book_with_page_read_more_than_page_count(self):
    url = f"{self.BASE_URL}/books/"
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
    response = self.client.post(url, data, format="json")
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_get_all_books(self):
    url = f"{self.BASE_URL}/books/"
    response = self.client.get(url, format="json")
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_get_detail_book_with_correct_id(self):
    book = Book.objects.create(
      name = "Recedivies",
      year = 2020,
      author = "Rois",
      summary = "Nice",
      publisher = "Tono",
      pageCount = 400,
      readPage = 200,
      finished = False,
      reading = False,
    )
    url = f"{self.BASE_URL}/books/{book.id}"
    response = self.client.get(url, format="json")
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_get_detail_book_with_invalid_id(self):
    url = f"{self.BASE_URL}/books/xxxxxxxx"
    response = self.client.get(url, format="json")
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_update_book_with_complete_data(self):
    book = Book.objects.create(
      name = "Recedivies",
      year = 2020,
      author = "Rois",
      summary = "Nice",
      publisher = "Tono",
      pageCount = 400,
      readPage = 200,
      finished = False,
      reading = False,
    )
    updated_data = {
      "name": "Recedivies09",
      "year": 2021,
      "author": "Rois",
      "summary": "Niceeeee!",
      "publisher": "Tono",
      "pageCount": 400,
      "readPage": 300,
      "finished": True,
      "reading": True,
    }
    url = f"{self.BASE_URL}/books/{book.id}"
    response = self.client.put(url, updated_data, format="json")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
  
  def test_update_book_without_name(self):
    book = Book.objects.create(
      name = "Recedivies",
      year = 2020,
      author = "Rois",
      summary = "Nice",
      publisher = "Tono",
      pageCount = 400,
      readPage = 200,
      finished = False,
      reading = False,
    )
    updated_data = {
      "name": "",
      "year": 2021,
      "author": "Rois",
      "summary": "Niceeeee!",
      "publisher": "Tono",
      "pageCount": 400,
      "readPage": 300,
      "finished": True,
      "reading": True,
    }
    url = f"{self.BASE_URL}/books/{book.id}"
    response = self.client.put(url, updated_data, format="json")
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_update_book_with_page_read_more_than_page_count(self):
    book = Book.objects.create(
      name = "Recedivies",
      year = 2020,
      author = "Rois",
      summary = "Nice",
      publisher = "Tono",
      pageCount = 400,
      readPage = 200,
      finished = False,
      reading = False,
    )
    updated_data = {
      "name": "Recedivies09",
      "year": 2021,
      "author": "Rois",
      "summary": "Niceeeee!",
      "publisher": "Tono",
      "pageCount": 400,
      "readPage": 500,
      "finished": True,
      "reading": True,
    }
    url = f"{self.BASE_URL}/books/{book.id}"
    response = self.client.put(url, updated_data, format="json")
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_update_book_with_invalid_id(self):
    updated_data = {
      "name": "Recedivies09",
      "year": 2021,
      "author": "Rois",
      "summary": "Niceeeee!",
      "publisher": "Tono",
      "pageCount": 400,
      "readPage": 300,
      "finished": True,
      "reading": True,
    }
    url = f"{self.BASE_URL}/books/xxxxx"
    response = self.client.put(url, updated_data, format="json")
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_delete_with_correct_id(self):
    book = Book.objects.create(
      name = "Recedivies",
      year = 2020,
      author = "Rois",
      summary = "Nice",
      publisher = "Tono",
      pageCount = 400,
      readPage = 200,
      finished = False,
      reading = False,
    )
    url = f"{self.BASE_URL}/books/{book.id}"
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
  def test_delete_with_invalid_id(self):
    book = Book.objects.create(
      name = "Recedivies",
      year = 2020,
      author = "Rois",
      summary = "Nice",
      publisher = "Tono",
      pageCount = 400,
      readPage = 200,
      finished = False,
      reading = False,
    )
    url = f"{self.BASE_URL}/books/xxxxxx"
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_get_book_with_create_finished_book(self):
    book = Book.objects.create(
      name = "Recedivies",
      year = 2020,
      author = "Rois",
      summary = "Nice",
      publisher = "Tono",
      pageCount = 400,
      readPage = 200,
      finished = True,
      reading = True,
    )
    self.assertEqual(Book.objects.filter(finished=1).count(), 1)

  def test_create_unreading_book(self):
    book = Book.objects.create(
      name = "Recedivies",
      year = 2020,
      author = "Rois",
      summary = "Nice",
      publisher = "Tono",
      pageCount = 400,
      readPage = 200,
      finished = True,
      reading = True,
    )
    self.assertEqual(Book.objects.filter(reading=0).count(), 0)