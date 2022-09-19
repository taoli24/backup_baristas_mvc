from main import ma


class VenueSchema(ma.Schema):
    class Meta:
        fields = ("id", "venue_name", "address", "email", "abn", "contact_number", "manager_id")


venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)