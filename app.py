from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import datetime

app = Flask(__name__)

load_dotenv()

dbname = os.getenv("database")
username = os.getenv("user_name")
hostname = os.getenv("hostname")
password = os.getenv("password")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{hostname}/{dbname}' 
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)  
    published_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    author = db.relationship('Author', back_populates='books')
    genres = db.relationship('Genre', secondary='book_genre', backref='books')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author.to_dict(),  # Include author information
            "published_at": self.published_at.strftime('%Y-%m-%d %H:%M:%S') if self.published_at else None,
        }


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', back_populates='author', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class BookGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return jsonify([author.to_dict() for author in authors])

@app.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    author = Author.query.get_or_404(author_id)
    return jsonify(author.to_dict())

@app.route('/genres', methods=['GET'])
def get_genres():
    genres = Genre.query.all()
    return jsonify([genre.to_dict() for genre in genres])

@app.route('/genres/<int:genre_id>', methods=['GET'])
def get_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return jsonify(genre.to_dict())

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    title = data.get("title")
    author_name = data.get("author")
    genre_name = data.get("genre")
    
    if not author_name:
        return jsonify({"error": "Author name is required"}), 400
    
    if not genre_name:
        return jsonify({"error": "Genre name is required"}), 400
    
    # Check if the author already exists in the database
    author = Author.query.filter_by(name=author_name).first()
    if not author:
        # If the author doesn't exist, create a new author
        author = Author(name=author_name)
        db.session.add(author)
    
    # Check if the genre already exists in the database
    genre = Genre.query.filter_by(name=genre_name).first()
    if not genre:
        # If the genre doesn't exist, create a new genre
        genre = Genre(name=genre_name)
        db.session.add(genre)

    # Create the book with the provided title, author, and genre
    book = Book(title=title, author=author, genres=[genre])
    db.session.add(book)
    db.session.commit()
    
    return jsonify(book.to_dict()), 201


@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    author = Author(**data)
    db.session.add(author)
    db.session.commit()
    return jsonify(author.to_dict()), 201

@app.route('/genres', methods=['POST'])
def create_genre():
    data = request.get_json()
    genre = Genre(**data)
    db.session.add(genre)
    db.session.commit()
    return jsonify(genre.to_dict()), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get_or_404(book_id)
    for key, value in data.items():
        setattr(book, key, value)
    db.session.commit()
    return jsonify(book.to_dict())

@app.route('/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    data = request.get_json()
    author = Author.query.get_or_404(author_id)
    for key, value in data.items():
        setattr(author, key, value)
    db.session.commit()
    return jsonify(author.to_dict())

@app.route('/genres/<int:genre_id>', methods=['PUT'])
def update_genre(genre_id):
    data = request.get_json()
    genre = Genre.query.get_or_404(genre_id)
    for key, value in data.items():
        setattr(genre, key, value)
    db.session.commit()
    return jsonify(genre.to_dict())

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

@app.route('/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    return '', 204

@app.route('/genres/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    db.session.delete(genre)
    db.session.commit()
    return '', 204

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
