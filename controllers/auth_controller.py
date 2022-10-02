from flask_jwt_extended import create_access_token
from main import db, bcrypt
from flask import Blueprint, request, abort, jsonify
from datetime import timedelta
from schemas import barista_schema, manager_schema
from models import Barista, Manager

auth = Blueprint("auth", __name__, url_prefix="/auth")


# user login - user is the worker
@auth.route("/login", methods=["POST"])
def user_login():
    user_fields = barista_schema.load(request.json, partial=True)
    user = Barista.query.filter_by(username=user_fields["username"]).first()
    # check if user exist and password correct
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Invalid username or password.")

    # create access token, set expiry to 1 day
    expiry = timedelta(days=1)
    token = create_access_token(identity=f"user{user.id}", expires_delta=expiry)

    return jsonify({"username": user.username, "access_token": token})


# register new user
@auth.route("/register", methods=["POST"])
def register_user():
    user_fields = barista_schema.load(request.json)

    # Check if username exist
    # if username already exist, abort operation
    if Barista.query.filter_by(username=user_fields["username"]).first():
        return abort(400, description="Username already exist in the database.")

    # Create the user instance
    new_user = Barista(
        username=user_fields["username"],
        password=bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8"),
        first_name=user_fields["first_name"],
        last_name=user_fields["last_name"],
        email=user_fields["email"],
        contact_number=user_fields["contact_number"],
        address=user_fields["address"],
    )

    db.session.add(new_user)
    db.session.commit()

    # Create token expire in 24 hours
    expire = timedelta(days=1)
    token = create_access_token(identity=f"user{new_user.id}", expires_delta=expire)

    return jsonify({"username": new_user.username, "access_token": token}), 201


# Manager login
@auth.route("/manager/login", methods=["POST"])
def manager_login():
    manager_fields = manager_schema.load(request.json, partial=True)
    manager = Manager.query.filter_by(username=manager_fields["username"]).first()
    # check if user exist and password correct
    if not manager or not bcrypt.check_password_hash(manager.password, manager_fields["password"]):
        return abort(401, description="Invalid username or password.")

    # Create token expire in 24 hours
    expiry = timedelta(days=1)
    token = create_access_token(identity=f"manager{manager.id}", expires_delta=expiry)

    return jsonify({"username": manager.username, "access_token": token})


# Register new manager
@auth.route("/manager/register", methods=["POST"])
def register_manager():
    manager_fields = manager_schema.load(request.json)
    # Check if manager already existed in the database
    manager = Manager.query.filter_by(username=manager_fields["username"]).first()

    # Return error if username already exist
    if manager:
        return abort(400, description="Manager with the same username already exist in the database.")

    new_manager = Manager(
        username=manager_fields["username"],
        password=bcrypt.generate_password_hash(manager_fields["password"]).decode("utf-8"),
        first_name=manager_fields["first_name"],
        last_name=manager_fields["last_name"],
        email=manager_fields["email"],
        contact_number=manager_fields["contact_number"]
    )

    db.session.add(new_manager)
    db.session.commit()

    # Create token expire in 24 hours
    expiry = timedelta(days=1)
    token = create_access_token(identity=f"manager{new_manager.id}", expires_delta=expiry)

    return jsonify({"username": new_manager.username, "access_token": token}), 201
