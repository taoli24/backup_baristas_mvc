from main import db
from models import Barista
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from schemas import barista_schema
from .helper_functions import authenticate_role_only

users = Blueprint("users", __name__, url_prefix="/users")


# User retrieve/update their information
@users.route("/", methods=["GET", "PUT"])
@jwt_required()
@authenticate_role_only(role="user")
def get_update_user():
    user = Barista.query.get(get_jwt_identity().replace("user", ""))

    if not user:
        return {"ERROR": "User does not exist."}, 400

    if request.method == "GET":
        return jsonify(barista_schema.dump(user))

    else:
        barista_fields = barista_schema.load(request.json, partial=True)

        user.first_name = barista_fields.get("first_name", user.first_name)
        user.last_name = barista_fields.get("last_name", user.last_name)
        user.email = barista_fields.get("email", user.email)
        user.contact_number = barista_fields.get("contact_number", user.contact_number)
        user.address = barista_fields.get("address", user.address)

        db.session.commit()

        return jsonify(barista_schema.dump(user))
