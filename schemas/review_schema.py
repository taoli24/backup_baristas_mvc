from main import ma
from marshmallow import fields
from marshmallow.validate import OneOf, Length


# noinspection PyTypeChecker
class ReviewSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "comments", "rating", "barista", "job")

    barista = fields.Nested("BaristaSchema", exclude=("username", "password", "reviews"))
    job = fields.Nested("JobSchema", exclude=("barista",))
    rating = fields.Int(required=True, strict=True, validate=OneOf(choices=(1, 2, 3, 4, 5)))
    comments = fields.Str(required=True, validate=Length(max=200))


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
