# Book API
This is a simple RESTful API for managing books, authors, and genres using Flask and SQLAlchemy.

## Requirements
- Python 3.x
- PostgreSQL
- flask 
- sqlalchemy

## Setup
1. Clone the repository:

   `git clone https://github.com/ChloeCudjoe/book-inventory.git`

2. Install dependancies:
 `pip install -r requirements.txt`

3. Create a PostgreSQL database and update the .env file with your database credentials.

4. Run the application:
  `python app.py`

## Endpoints
- GET /books: Get all books
- GET /books/<book_id>: Get a specific book
- POST /books: Create a new book
- PUT /books/<book_id>: Update a book
- DELETE /books/<book_id>: Delete a book
*Similar endpoints are available for authors and genres.*

## USAGE
using the rest client extension to test the endpoints

`POST http://127.0.0.1:5000/books HTTP/1.1
content-type: application/json`

`{
    "title": "purple hibiscus",
    "author": "chimamba",
    "genre": "hsitorical fictional novel"
}`
### Response
**Creating a new book**
`Server: Werkzeug/3.0.2 Python/3.12.0
Date: Sat, 11 May 2024 16:09:12 GMT
Content-Type: application/json
Content-Length: 140
Connection: close`

`{
  "author": {
    "id": 1,
    "name": "chimamba"
  },
  "id": 3,
  "published_at": "2024-05-11 16:09:12",
  "title": "purple hibiscus"
}`

