from main import ma
from marshmallow.validate import Length


class ManagerSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "username", "password", "first_name", "last_name", "email", "contact_number", "join_date")
        load_only = ("username", "password", "join_date")

    # validate password
    password = ma.String(validate=Length(min=8))


manager_schema = ManagerSchema()
