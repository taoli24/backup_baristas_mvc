from flask import Blueprint, jsonify, request, abort
from main import db
from models import Job, Venue
from schemas import jobs_schema, job_schema

jobs = Blueprint("jobs", __name__, url_prefix="/jobs")


# get all available jobs
@jobs.route("/", methods=["GET"])
def get_all_available_jobs():
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
def new_job(venue_id):
    venue = Venue.query.get(venue_id)
    if not venue:
        return abort(400, description="Venue does not exist")
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
    return jsonify(job_schema.dump(job))


# Delete a job
@jobs.route("/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return abort(400, description="Job does not exist")

    db.session.delete(job)
    db.session.commit()

    return jsonify(job_schema.dump(job))


# Update a job
@jobs.route("<int:job_id>", methods=["PUT"])
def update_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return abort(400, description="Job does not exist")

    job_fields = job_schema.load(request.json)
    job.description = job_fields.get("description", job.description)
    job.date = job_fields.get("date", job.date)
    job.start_time = job_fields.get("start_time", job.start_time)
    job.finish_time = job_fields.get("finish_time", job.finish_time)
    job.pay_rate = job_fields.get("pay_rate", job.pay_rate)

    db.session.commit()
    return jsonify(job_schema.dump(job))
