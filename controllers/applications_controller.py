from models import Application, Job, Venue
from main import db
from flask import Blueprint, jsonify, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from .helper_functions import authenticate_role_only, set_no_expire
from schemas import applications_schema, user_applications_schema, user_application_schema

applications = Blueprint("applications", __name__, url_prefix="/applications")


# View all applications of jobs managed by signed in managers
@applications.route("/", methods=["GET"])
@jwt_required()
@authenticate_role_only(role="manager")
def get_applications():
    # Get all applications managed by the manager
    jobs = db.session.query(Application, Job, Venue) \
        .join(Job, Application.job_id == Job.id) \
        .join(Venue, Job.venue_id == Venue.id) \
        .filter(Venue.manager_id == get_jwt_identity().replace("manager", "")).all()

    return jsonify(applications_schema.dump(application[0] for application in jobs))


# User view their applications
@applications.route("/user")
@jwt_required()
@authenticate_role_only(role="user")
def get_user_application():
    user_id = get_jwt_identity().replace("user", "")
    application_list = Application.query.filter_by(barista_id=user_id).all()

    return jsonify(user_applications_schema.dump(application_list))


# User delete/withdraw application if status is pending
@applications.route("/user/<int:application_id>", methods=["DELETE"])
@jwt_required()
@authenticate_role_only(role="user")
def delete_application(application_id):
    user_application = Application.query.get(application_id)

    if not user_application:
        return abort(400, description="Application does not exist.")

    if str(user_application.barista_id) != get_jwt_identity().replace("user", ""):
        return abort(401, description="You don't have permission to delete this application.")

    if user_application.status != "pending":
        return abort(401, description="Only applications with pending status can be withdrawn.")

    with set_no_expire():
        db.session.delete(user_application)
        db.session.commit()
    return jsonify(user_application_schema.dump(user_application))

