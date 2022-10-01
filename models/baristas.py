from main import db
from datetime import date


class Barista(db.Model):
    __tablename__ = "baristas"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    contact_number = db.Column(db.String(), nullable=False)
    address = db.Column(db.String())
    join_date = db.Column(db.Date(), default=date.today())
    rating = db.Column(db.Float(), default=0.0)
    number_ratings = db.Column(db.Integer, default=0)
    applications = db.relationship("Application", backref="barista", cascade="all, delete")
    reviews = db.relationship("Review", backref="barista", cascade="all, delete")
    jobs = db.relationship("Job", backref="barista")  # jobs should be kept when barista is deleted
