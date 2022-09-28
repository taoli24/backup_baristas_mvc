from main import ma
from marshmallow import fields


# noinspection PyTypeChecker
class ApplicationSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "job_id", "job", "barista_id", "barista", "status",)
        load_only = ("job_id", "barista_id")

    job = fields.Nested("JobSchema")
    barista = fields.Nested("BaristaSchema", exclude=("username", "password", "join_date"))


# noinspection PyTypeChecker
class UserApplicationSchema(ApplicationSchema):
    # Overwrite job class attribute to exclude other applicants' information
    job = fields.Nested("JobSchema", exclude=("barista",))


application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)

# Schema allow user view their own application without viewing other applicants information
user_application_schema = UserApplicationSchema()
user_applications_schema = UserApplicationSchema(many=True)
