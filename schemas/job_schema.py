from main import ma
from marshmallow import fields


class JobSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "description", "date", "start_time", "finish_time", "pay_rate", "status", "barista", "venue")

    barista = fields.Nested("BaristaSchema", exclude=("username", "password"))
    venue = fields.Nested("VenueSchema", exclude=("jobs", "manager"))


job_schema = JobSchema()
jobs_schema = JobSchema(many=True)

