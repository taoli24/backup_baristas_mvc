from flask import Blueprint, request, abort, jsonify
from models import Venue
from schemas import venue_schema, venues_schema
from main import db

venues = Blueprint("venues", __name__, url_prefix="/venues")


# Add new venues
@venues.route("/", methods=["POST"])
def add_venue():
    venue_fields = venue_schema.load(request.json)
    # check if venue already exist
    venue = Venue.query.filter_by(venue_name=venue_fields["venue_name"]).first()
    if venue:
        return abort(400, description="venue with the same name already exist.")

    new_venue = Venue(
        venue_name=venue_fields["venue_name"],
        address=venue_fields["address"],
        email=venue_fields["email"],
        abn=venue_fields["abn"],
        contact_number=venue_fields["contact_number"]
    )

    db.session.add(new_venue)
    db.session.commit()

    return jsonify(venue_schema.dump(new_venue))
