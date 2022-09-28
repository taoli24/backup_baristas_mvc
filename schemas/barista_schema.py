from main import ma
from marshmallow.validate import Length, Email
from marshmallow import fields


class BaristaSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "username", "password", "first_name", "last_name", "email", "contact_number", "address", "join_date", "rating", "reviews")
        load_only = ("username", "password", "join_date")

    reviews = fields.List(fields.Nested("ReviewSchema", exclude=("barista", "job")))
    # validation of fields
    username = ma.String(required=True)
    password = ma.String(validate=Length(min=8), required=True)
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.String(validate=Email(), required=True)
    contact_number = ma.String(required=True)
    address = ma.String(required=True)


barista_schema = BaristaSchema(exclude=("reviews",))
# Barista schema with serialized children reviews
barista_review_schema = BaristaSchema(exclude=("address",))
