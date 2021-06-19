import json
import requests

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0MTAyMzYwLCJqdGkiOiJiZjRhNzliOTFmMGY0ZjZhODMxNmIxN2Q2MTY2ZDg3NiIsInVzZXJfaWQiOjh9._QStDlxYxz2hFnnv4DapabN3KDChws9MHuZQNfzPkjg"
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json' 
}

# get all books - no token needed
books = requests.get('http://127.0.0.1:8000/api/books/')
print(books.json())

# create new book
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
book = requests.get(f'http://127.0.0.1:8000/api/books/{bookid}')
print(book.json())

# update book
payload = json.dumps({
    'name': 'book-name-updated',
    'year': 2022,
    'author': 'author-name-updated',
    'summary': 'book-summary-updated',
    'publisher': 'book-publisher-updated',
    'pageCount': 400,
    'readPage': 399
})
updated_book = requests.put(f'http://127.0.0.1:8000/api/books/{bookid}',
    data=payload,
    headers=headers
)
print(updated_book.json())

# delete book
delete_book = requests.delete(f'http://127.0.0.1:8000/api/books/{bookid}',
    headers=headers
)
print(delete_book.json())