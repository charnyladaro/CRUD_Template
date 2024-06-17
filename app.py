# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import db, Book, Review

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# Create operation - Add a new book
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        new_book = Book(title=title, author=author)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html")


# Read operation - Display all books
@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books=books)


# Update operation - Edit an existing book
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    book = Book.query.get_or_404(id)
    if request.method == "POST":
        book.title = request.form["title"]
        book.author = request.form["author"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", book=book)


# Delete operation - Delete an existing book
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("index"))


# Read operation - Display all reviews for a book
@app.route("/reviews/<int:book_id>")
def reviews(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    return render_template("reviews/index.html", book=book, reviews=reviews)


# Create operation - Add a new review
@app.route("/reviews/add/<int:book_id>", methods=["GET", "POST"])
def add_review(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == "POST":
        content = request.form["content"]
        new_review = Review(content=content, book_id=book_id)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for("reviews", book_id=book_id))
    return render_template("reviews/add.html", book=book)


# Update operation - Edit an existing review
@app.route("/reviews/edit/<int:book_id>/<int:id>", methods=["GET", "POST"])
def edit_review(book_id, id):
    review = Review.query.get_or_404(id)
    if request.method == "POST":
        review.content = request.form["content"]
        db.session.commit()
        return redirect(url_for("reviews", book_id=book_id))
    return render_template("reviews/edit.html", review=review)


# Delete operation - Show delete confirmation page
@app.route("/reviews/delete/<int:book_id>/<int:id>", methods=["GET", "POST"])
def delete_review(book_id, id):
    review = Review.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(review)
        db.session.commit()
        return redirect(url_for("reviews", book_id=book_id))
    return render_template("reviews/delete.html", review=review)


if __name__ == "__main__":
    app.run(debug=True)
