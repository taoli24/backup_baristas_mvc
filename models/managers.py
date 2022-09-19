from main import db
from datetime import date


class Manager(db.Model):
    __tablename__ = "managers"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    contact_number = db.Column(db.String(), nullable=False)
    join_date = db.Column(db.Date(), default=date.today())
    venues = db.relationship("Venue", backref="manager", cascade="all, delete")
