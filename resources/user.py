from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Book, BorrowRequest

user_bp = Blueprint('user', __name__)

@user_bp.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    books = Book.query.all()
    return jsonify([{"id": book.id, "title": book.title, "author": book.author, "available": book.available} for book in books]), 200

@user_bp.route('/borrow', methods=['POST'])
@jwt_required()
def borrow_book():
    current_user = get_jwt_identity()
    data = request.json

    book_id = data.get('book_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    # Check book availability
    overlapping_request = BorrowRequest.query.filter(
        BorrowRequest.book_id == book_id,
        BorrowRequest.end_date >= start_date,
        BorrowRequest.start_date <= end_date,
        BorrowRequest.status == "approved"
    ).first()

    if overlapping_request:
        return jsonify({"error": "Book is not available during the requested dates"}), 400

    borrow_request = BorrowRequest(
        user_id=current_user['id'],
        book_id=book_id,
        start_date=start_date,
        end_date=end_date
    )

    db.session.add(borrow_request)
    db.session.commit()

    return jsonify({"message": "Borrow request submitted"}), 201
