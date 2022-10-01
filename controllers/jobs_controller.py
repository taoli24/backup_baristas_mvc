from flask import Blueprint, jsonify, request, abort
from main import db
from models import Job, Venue, Application, Review, Barista
from schemas import jobs_schema, job_schema, application_schema, review_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from .helper_functions import authenticate_role_only

jobs = Blueprint("jobs", __name__, url_prefix="/jobs")


# get all available jobs/optional search
# currently jobs can be filtered by venue location(city) or min_rate
@jobs.route("/", methods=["GET"])
def get_all_available_jobs():
    if request.query_string:
        job_list = db.session.query(Job, Venue) \
            .join(Venue, Job.venue_id == Venue.id) \
            .filter(Job.pay_rate > request.args.get("min_rate", 0),
                    Job.status == "To be fulfilled",
                    Venue.city == request.args.get("location").capitalize()).all()[0] \
            if request.args.get("location") else \
            Job.query.filter(Job.pay_rate > request.args.get("min_rate", 0),
                             Job.status == "To be fulfilled")

    else:
        job_list = Job.query.filter_by(status="To be fulfilled").all()
    return jsonify(jobs_schema.dump(job_list))


# get all available jobs of a venue
@jobs.route("/<int:venue_id>", methods=["GET"])
def get_all_available_jobs_per_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if not venue:
        return abort(400, description="venue does not exist")

    jobs_list = Job.query.filter_by(venue_id=venue_id).all()
    return jsonify(jobs_schema.dump(jobs_list))


# post new jobs
@jobs.route("/<int:venue_id>", methods=["POST"])
@jwt_required()
@authenticate_role_only(role="manager")
def new_job(venue_id):
    venue = Venue.query.get(venue_id)
    if not venue:
        return abort(400, description="Venue does not exist")

    # Check if manager has permission to post a job for this venue
    if not str(venue.manager_id) == get_jwt_identity().replace("manager", ""):
        return abort(401, description="You don't have permission to post for this venue.")

    job_fields = job_schema.load(request.json)
    job = Job(
        description=job_fields["description"],
        date=job_fields["date"],
        start_time=job_fields["start_time"],
        finish_time=job_fields["finish_time"],
        pay_rate=job_fields["pay_rate"],
        venue_id=venue_id
    )

    db.session.add(job)
    db.session.commit()
    return jsonify(job_schema.dump(job)), 201


# Delete a job
@jobs.route("/delete/<int:job_id>", methods=["DELETE"])
@jwt_required()
@authenticate_role_only(role="manager")
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return abort(400, description="Job does not exist")

    # Return error if manager id does not match
    job_venue = Venue.query.get(job.venue_id)
    if not str(job_venue.manager_id) == get_jwt_identity().replace("manager", ""):
        return abort(401, description="You don't have permission to delete this job.")

    db.session.delete(job)
    db.session.commit()

    return jsonify(job_schema.dump(job))


# Update a job
@jobs.route("<int:job_id>", methods=["PUT"])
@jwt_required()
@authenticate_role_only(role="manager")
def update_job(job_id):
    job = Job.query.get(job_id)
    # Check if job exist in the database
    if not job:
        return abort(400, description="Job does not exist")

    # Check if the job is managed by the manager
    job_venue = Venue.query.get(job.venue_id)

    if not str(job_venue.manager_id) == get_jwt_identity().replace("manager", ""):
        return abort(401, description="You don't have permission to update this job.")

    job_fields = job_schema.load(request.json)
    job.description = job_fields.get("description", job.description)
    job.date = job_fields.get("date", job.date)
    job.start_time = job_fields.get("start_time", job.start_time)
    job.finish_time = job_fields.get("finish_time", job.finish_time)
    job.pay_rate = job_fields.get("pay_rate", job.pay_rate)

    db.session.commit()
    return jsonify(job_schema.dump(job))


# Apply for job
@jobs.route("<int:job_id>/apply", methods=["POST"])
@jwt_required()
@authenticate_role_only(role="user")
def apply_job(job_id):
    job = Job.query.get(job_id)
    if not job or job.status == "fulfilled":
        return abort(400, description="The job does not exist or has been fulfilled.")

    application = Application(
        job_id=job_id,
        barista_id=get_jwt_identity().replace("user", "")
    )

    db.session.add(application)
    db.session.commit()
    return jsonify(application_schema.dump(application))


# Approve applicant
@jobs.route("<int:job_id>/approve", methods=["PUT"])
@jwt_required()
@authenticate_role_only(role="manager")
def approve_applicant(job_id):
    # Check if job exist
    job = Job.query.get(job_id)
    if not job:
        return abort(400, description="Job does not exist.")
    # Check if the job is managed by the manager
    job_venue = Venue.query.get(job.venue_id)
    if not str(job_venue.manager_id) == get_jwt_identity().replace("manager", ""):
        return abort(401, description="You don't have permission to update this job.")

    # Check if there are applicants
    applications = Application.query.filter_by(job_id=job_id).all()
    if not len(applications):
        return jsonify({"ERROR": "No applications were found."})

    barista_id = application_schema.load(request.json)["barista_id"]
    # Modify application status
    for application in applications:
        if application.barista_id == barista_id:
            application.status = "approved"
        else:
            application.status = "unsuccessful"

    # Change job status to fulfilled, also assign barista_id to job
    job.status = "fulfilled"
    job.barista_id = barista_id

    db.session.commit()
    return jsonify(job_schema.dump(job))


# Review job performed by baristas
@jobs.route("/<int:job_id>/review", methods=["POST"])
@jwt_required()
@authenticate_role_only(role="manager")
def review_job(job_id):
    job = Job.query.get(job_id)
    print(job)
    if not job:
        return abort(400, description="Job does not exist.")

    if job.status != "fulfilled":
        return abort(401, description="You can only leave review for fulfilled job.")

    job_venue = Venue.query.get(job.venue_id)

    if str(job_venue.manager_id) != get_jwt_identity().replace("manager", ""):
        return abort(401, description="You do not have permission to review this job.")

    # check if a job has been reviewed
    review = Review.query.filter_by(job_id=job_id).first()
    if review:
        return abort(401, description="Review has already been left for this job.")

    review_fields = review_schema.load(request.json)

    new_review = Review(
        comments=review_fields["comments"],
        rating=review_fields["rating"],
        barista_id=job.barista_id,
        job_id=job_id
    )

    db.session.add(new_review)

    # Access barista model and update rating
    batista = Barista.query.get(job.barista_id)
    batista.number_ratings = batista.number_ratings + 1
    batista.rating = (batista.rating * (batista.number_ratings - 1) + review_fields["rating"]) / batista.number_ratings

    db.session.commit()

    return jsonify(review_schema.dump(new_review))
