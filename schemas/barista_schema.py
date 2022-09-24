from main import ma
from marshmallow.validate import Length


class BaristaSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "username", "password", "first_name", "last_name", "email", "contact_number", "address", "join_date", "rating")
        load_only = ("username", "password", "address", "join_date")

    # validate password
    password = ma.String(validate=Length(min=8))


barista_schema = BaristaSchema()
