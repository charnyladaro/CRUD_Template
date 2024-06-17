# models.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    reviews = db.relationship("Review", backref="book", lazy=True)

    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}')"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)

    def __repr__(self):
        return f"Review(content='{self.content}')"
