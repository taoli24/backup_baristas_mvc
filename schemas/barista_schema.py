from main import ma
from marshmallow.validate import Length, Email


class BaristaSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "username", "password", "first_name", "last_name", "email", "contact_number", "address", "join_date", "rating")
        load_only = ("username", "password", "address", "join_date")

    # validation of fields
    username = ma.String(required=True)
    password = ma.String(validate=Length(min=8), required=True)
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.String(validate=Email(), required=True)
    contact_number = ma.String(required=True)
    address = ma.String(required=True)


barista_schema = BaristaSchema()
