import json
import requests

token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI2MTkwNDE5LCJqdGkiOiIxNmU2Y2RjMDg4OWU0N2MyOGE5M2FkMGQ2NjE5NjA4YiIsInVzZXJfaWQiOjE4fQ.o1ISEiIV-3GSXDfoUb3k8jH6XMTPt5SDLNwJ8oU0zKc"
headers = {
    'Authorization': token,
    'Content-Type': 'application/json'
}

# create new book
books = requests.get('http://127.0.0.1:8000/api/books/')
print(books.json())

payload = json.dumps({
    'name': 'book-name',
    'year': 2021,
    'author': 'author-name',
    'summary': 'book-summary',
    'publisher': 'book-publisher',
    'pageCount': 400,
    'readPage': 0
})
new_book = requests.post('http://127.0.0.1:8000/api/books/',
                         data=payload,
                         headers=headers
                         )
new_book = new_book.json()

# get book - no token needed
bookid = new_book['data']['bookId']
book = requests.get(f'http://127.0.0.1:8000/api/books/{bookid}/')
print(book.json())

# update book
payload = json.dumps({
    'name': 'book-name',
    'year': 2021,
    'author': 'author-name',
    'summary': 'book-summary',
    'publisher': 'book-publisher',
    'pageCount': 400,
    'readPage': 399
})
updated_book = requests.put(f'http://127.0.0.1:8000/api/books/{bookid}/',
                            data=payload,
                            headers=headers
                            )
print(updated_book.json())

# delete book
delete_book = requests.delete(f'http://127.0.0.1:8000/api/books/{bookid}',
                              headers=headers
                              )
print(delete_book.json())
