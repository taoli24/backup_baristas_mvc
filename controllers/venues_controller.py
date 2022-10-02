from flask import Blueprint, request, abort, jsonify
from models import Venue
from schemas import venue_schema, venues_schema
from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from .helper_functions import authenticate_role_only, set_no_expire

venues = Blueprint("venues", __name__, url_prefix="/venues")


# Add new venue
@venues.route("/", methods=["POST"])
@jwt_required()
@authenticate_role_only(role="manager")
def add_venue():
    venue_fields = venue_schema.load(request.json)
    # check if venue already exist
    venue = Venue.query.filter_by(venue_name=venue_fields["venue_name"]).first()
    if venue:
        return abort(400, description="Venue with the same name already exist.")

    new_venue = Venue(
        venue_name=venue_fields["venue_name"],
        address=venue_fields["address"],
        city=venue_fields["city"],
        email=venue_fields["email"],
        abn=venue_fields["abn"],
        contact_number=venue_fields["contact_number"],
        manager_id=get_jwt_identity().replace("manager", "")
    )

    db.session.add(new_venue)
    db.session.commit()

    return jsonify(venue_schema.dump(new_venue)), 201


# get venues associate with current manager id
@venues.route("/", methods=["GET"])
@jwt_required()
@authenticate_role_only(role="manager")
def get_venues():
    manager_id = get_jwt_identity().replace("manager", "")
    venue_list = Venue.query.filter_by(manager_id=manager_id).all()

    return jsonify(venues_schema.dump(venue_list))


# Update a venue
@venues.route("/<int:venue_id>", methods=["PUT"])
@jwt_required()
@authenticate_role_only(role="manager")
def update_venue(venue_id):
    venue = Venue.query.get(venue_id)

    if not venue:
        return abort(400, description="Venue does not exist.")

    if str(venue.manager_id) != get_jwt_identity().replace("manager", ""):
        return abort(401, description="You do not have permission to update this venue.")

    venue_fields = venue_schema.load(request.json, partial=True)

    # Only update supplied fields
    venue.venue_name = venue_fields.get("venue_name", venue.venue_name)
    venue.address = venue_fields.get("address", venue.address)
    venue.email = venue_fields.get("email", venue.email)
    venue.abn = venue_fields.get("abn", venue.abn)
    venue.contact_number = venue_fields.get("contact_number", venue.contact_number)

    db.session.commit()
    return jsonify(venue_schema.dump(venue))


# Delete venue
@venues.route("/<int:venue_id>", methods=["DELETE"])
@jwt_required()
@authenticate_role_only(role="manager")
def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)

    if not venue:
        return abort(400, description="Venue does not exist.")

    if str(venue.manager_id) != get_jwt_identity().replace("manager", ""):
        return abort(401, description="You do not have permission to update this venue.")

    with set_no_expire():
        db.session.delete(venue)
        db.session.commit()

    return jsonify(venue_schema.dump(venue))
