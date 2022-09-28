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
def get_current_user():
    if request.method == "GET":
        user = Barista.query.get(get_jwt_identity().replace("user", ""))
        if not user:
            return {"ERROR": "User does not exist."}, 400

        return jsonify(barista_schema.dump(user))

    else:
        barista_fields = barista_schema.load(request.json)

        print(barista_fields)
