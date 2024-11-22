from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["LibraryDB"]
books_collection = db["Books"]

@app.route("/")
def home():
    books = list(books_collection.find({}, {"_id": 0}))
    return render_template("index.html", books=books)

@app.route("/add_book", methods=["POST"])
def add_book():
    title = request.form.get("title")
    author = request.form.get("author")
    isbn = request.form.get("isbn")

    if title and author and isbn:
        books_collection.insert_one({"title": title, "author": author, "isbn": isbn})
        return redirect(url_for("home"))
    else:
        return "Error: Please fill in all fields", 400

@app.route("/api/books", methods=["GET"])
def api_books():
    books = list(books_collection.find({}, {"_id": 0}))
    return jsonify(books)

if __name__ == "__main__":
    app.run(debug=True)
