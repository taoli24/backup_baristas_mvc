from main import ma
from marshmallow.validate import Length


class ManagerSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "first_name", "last_name", "email", "contact_number", "join_date")
        load_only = ("username", "password")

    # validate password
    password = ma.String(validate=Length(min=8))


manager_schema = ManagerSchema()
