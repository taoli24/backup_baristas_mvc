from main import ma
from marshmallow import fields


class ApplicationSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "job", "barista", "status")

    job = fields.Nested("JobSchema")
    barista = fields.Nested("BaristaSchema", exclude=("username", "password", "join_date"))


class UserApplicationSchema(ApplicationSchema):
    # Overwrite job class attribute to exclude other applicants' information
    job = fields.Nested("JobSchema", exclude=("barista",))


application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)

# Schema allow user view their own application without viewing other applicants information
user_application_schema = UserApplicationSchema()
user_applications_schema = UserApplicationSchema(many=True)
