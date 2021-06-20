from django.urls import path

from .views import (
	ListCreateBook,
	ListUpdateDeleteBookById, 
)

urlpatterns = [
	path('books/', ListCreateBook.as_view()),
	path('books/<str:pk>/', ListUpdateDeleteBookById.as_view()),
]