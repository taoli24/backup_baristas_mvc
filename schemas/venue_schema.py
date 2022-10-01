from main import ma
from marshmallow import fields
from marshmallow.validate import Email


# noinspection PyTypeChecker
class VenueSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "venue_name", "address", "city", "email", "abn", "contact_number", "manager", "jobs")

    # Nested schemas
    manager = fields.Nested("ManagerSchema", exclude=("username", "password",))
    jobs = fields.List(fields.Nested("JobSchema", exclude=("venue",)))

    # Validation of fields
    venue_name = ma.String(required=True)
    address = ma.String(required=True)
    city = ma.String(required=True)
    email = ma.String(required=True, validate=Email())
    abn = ma.String(required=True),
    contact_number = ma.String(required=True)


venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)
