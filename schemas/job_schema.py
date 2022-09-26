from main import ma
from marshmallow import fields


class JobSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "description", "date", "start_time", "finish_time", "pay_rate", "status", "barista", "venue")

    # Nested schemas
    barista = fields.Nested("BaristaSchema", exclude=("username", "password"))
    venue = fields.Nested("VenueSchema", exclude=("jobs", "manager"))
    # Validations of fields
    description = ma.String(required=True)
    date = ma.Date(required=True)
    start_time = ma.Time(required=True)
    finish_time = ma.Time(required=True)
    pay_rate = ma.Integer(required=True)


job_schema = JobSchema()
jobs_schema = JobSchema(many=True)

