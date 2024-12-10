from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, User
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')  # Default role is user

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password, role=role)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify({"access_token": token}), 200

    return jsonify({"error": "Invalid email or password"}), 401
