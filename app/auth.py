from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from .models import User
from . import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "User already exists"}), 409

    hashed_pw = generate_password_hash(data["password"])
    user = User(username=data["username"], password=hashed_pw)
    db.session.add(user)
    db.session.commit()

    return jsonify(message="User created successfully"), 201

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # FIX: convert user.id to string to prevent 422 error
    token = create_access_token(identity=str(user.id))
    return jsonify(access_token=token), 200
