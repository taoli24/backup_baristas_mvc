from main import ma
from marshmallow.validate import Length, Email


class ManagerSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "username", "password", "first_name", "last_name", "email", "contact_number", "join_date")
        load_only = ("username", "password", "join_date")

    # validate password
    username = ma.String(required=True)
    password = ma.String(required=True, validate=Length(min=8))
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.String(required=True, validate=Email())
    contact_number = ma.String(required=True)


manager_schema = ManagerSchema()
