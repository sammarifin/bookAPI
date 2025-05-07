from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Book, Loan
from . import db

main = Blueprint("main", __name__)

@main.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify([{"id": b.id, "title": b.title, "author": b.author} for b in books])

@main.route("/books", methods=["POST"])
@jwt_required()
def add_book():
    data = request.get_json()
    if not isinstance(data.get("title"), str) or not isinstance(data.get("author"), str):
        return jsonify({"msg": "title and author must be strings"}), 422
    
    book = Book(title=data["title"], author=data["author"])
    db.session.add(book)
    db.session.commit()
    return jsonify(message="Book added"), 201


@main.route("/loans", methods=["POST"])
@jwt_required()
def borrow_book():
    user_id = get_jwt_identity()
    data = request.get_json()
    loan = Loan(user_id=user_id, book_id=data["book_id"])
    db.session.add(loan)
    db.session.commit()
    return jsonify(message="Book borrowed"), 201

@main.route("/loans", methods=["GET"])
@jwt_required()
def my_loans():
    user_id = get_jwt_identity()
    loans = Loan.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "book_id": l.book_id,
            "book_title": l.book.title,
            "loan_date": l.loan_date.isoformat()
        } for l in loans
    ])
