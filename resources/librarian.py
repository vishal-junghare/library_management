from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Book, BorrowRequest, User

librarian_bp = Blueprint('librarian', __name__)

@librarian_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    users = User.query.all()
    return jsonify([{"id": user.id, "email": user.email, "role": user.role} for user in users]), 200

@librarian_bp.route('/borrow_requests', methods=['GET'])
@jwt_required()
def view_borrow_requests():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    requests = BorrowRequest.query.all()
    return jsonify([{
        "id": req.id,
        "user": req.user.email,
        "book": req.book.title,
        "start_date": req.start_date,
        "end_date": req.end_date,
        "status": req.status
    } for req in requests]), 200

@librarian_bp.route('/borrow_requests/<int:request_id>', methods=['PUT'])
@jwt_required()
def update_borrow_request(request_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    status = data.get('status')

    borrow_request = BorrowRequest.query.get(request_id)
    if not borrow_request:
        return jsonify({"error": "Request not found"}), 404

    borrow_request.status = status
    if status == "approved":
        borrow_request.book.available = False

    db.session.commit()
    return jsonify({"message": "Request updated"}), 200
