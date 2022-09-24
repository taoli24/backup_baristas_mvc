from main import ma
from marshmallow import fields


class VenueSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "venue_name", "address", "email", "abn", "contact_number", "manager", "jobs")

    manager = fields.Nested("ManagerSchema", exclude=("username", "password",))
    jobs = fields.List(fields.Nested("JobSchema", exclude=("venue",)))


venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)
