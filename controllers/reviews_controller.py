from main import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .helper_functions import authenticate_role_only
from models import Barista, Review, Job, Venue
from schemas import barista_review_schema, review_schema
from .helper_functions import set_no_expire

reviews = Blueprint("reviews", __name__, url_prefix="/reviews")


# Get all reviews and scores of a barista, only venue manager should have access to this
@reviews.route("/barista/<int:barista_id>", methods=["GET"])
@jwt_required()
@authenticate_role_only(role="manager")
def get_barista_review(barista_id):
    barista = Barista.query.get(barista_id)

    # Check if barista exist
    if not barista:
        return {"Error", "Barista does not exist in the database."}, 400

    return jsonify(barista_review_schema.dump(barista))


# Update/delete review
@reviews.route("/<int:review_id>", methods=["PUT", "DELETE"])
@jwt_required()
@authenticate_role_only(role="manager")
def modify_review(review_id):
    # Validate manager
    review = db.session.query(Review, Job, Venue) \
                .join(Job, Review.job_id == Job.id) \
                .join(Venue, Job.venue_id == Venue.id) \
                .filter(Review.id == review_id).first()

    if str(review[2].manager_id) != get_jwt_identity().replace("manager", ""):
        return {"Error": "You don't have permission to modify this review."}, 401

    if request.method == "DELETE":
        with set_no_expire():
            db.session.delete(review[0])
            db.session.commit()
        return jsonify(review_schema.dump(review[0]))
    else:
        review_field = review_schema.load(request.json, partial=True)
        review[0].comments = review_field.get("comments", review[0].comments)
        if review_field["rating"] is not None:
            # Update barista rating in the barista table
            diff = review_field["rating"] - review[0].rating
            barista = Barista.query.get(review[0].barista_id)
            barista.rating = (barista.rating * barista.number_ratings + diff)/barista.number_ratings

            # Update rating of the review
            review[0].rating = review_field.get("rating", review[0].rating)
        db.session.commit()

        return jsonify(review_schema.dump(review[0]))


