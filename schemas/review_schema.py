from main import ma
from marshmallow import fields


class ReviewSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "comments", "rating", "barista", "job")

    barista = fields.Nested("BaristaSchema", exclude=("username", "password"))
    job = fields.Nested("JobSchema", exclude=("barista",))


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
